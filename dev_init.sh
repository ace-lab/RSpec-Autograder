build() { sudo docker build -t saasbook/pl-rspec-autograder . ; }
push() { sudo docker push saasbook/pl-rspec-autograder:latest ; }
buildPushDev() { sudo docker build -t saasbook/pl-rspec-autograder:dev . && sudo docker push saasbook/pl-rspec-autograder:dev ; }
buildPush() { build && push ; }

buildCont() { # build rspec-autograder:dev
    # only report errors
    hash="$(sudo docker build -q -t rspec-autograder:dev .  | cut -d: -f2)"
    echo \> Image name/hash: rspec-autograder:dev / $hash
}

runImage() { # run rspec-autograder:dev
    cont="$(sudo docker run --network none --mount type=bind,source=`pwd`/.container_mount/grade,target=/grade -d rspec-autograder:dev /grader/run.py)"
    echo \> Container hash: $cont
    code="$(sudo docker container wait $cont)"
    echo \> Container exited with code $code
    return $code
}

clean_up() { # assuming $1 is the container hash
    sudo chown -R $USER .container_mount/grade/
    # destroy the container
    echo -n Deleting continer ...
    sudo docker container rm $1 > /dev/null
    echo done.
}

prep_mount() { # assuming $1 is the variants_dir (the question/tests/ directory)

    which jq > /dev/null
    if [[ $? != "0" ]]; then 
        echo "jq is required to run this script, please install and add it to your \$PATH"
        return 1
    fi

    echo "Preparing mount files ... "

    sudo rm -rf .container_mount

    # make all the necessary dirs
    mkdir .container_mount

    mkdir .container_mount/grade
    mkdir .container_mount/grade/data
    mkdir .container_mount/grade/serverFilesCourse
    mkdir .container_mount/grade/student
    mkdir .container_mount/grade/tests

    # load the variants
    # script_dir="$(pwd)/${0::-18}"
    variant_dir="$(pwd)/$1/"
    cp -r $variant_dir/* .container_mount/grade/tests/
    rm .container_mount/grade/tests/data.json
    rm .container_mount/grade/tests/expected.json

    # load submission files
    if [[ -f $variant_dir/data.json ]]; then
        cp $variant_dir/data.json .container_mount/grade/data/
    elif [[ -d $variant_dir/submission ]]; then
        cp -r $variant_dir/submission/* .container_mount/grade/student

        echo {\"submitted_answers\": {\"student-parsons-solution\": `jq -Rs . < .container_mount/grade/student/_submission_file`}} \
            > .container_mount/grade/data/data.json
        ## double-check that _submission_file isn't in /grade/student
        rm .container_mount/grade/student/_submission_file
    else 
        echo "No submission found: Exiting"
        return 1
    fi

    # now that the files are in place, install the packages
    pd=`pwd`
    cd $variant_dir/common
    bundle package --all-platforms --quiet > /dev/null #--without-production
    bundle install --local > /dev/null #--development
    cd $pd
}

compare() { # assuming $1 is the variant directory, $2 is the script directory
    # compare the result
    echo ========================= COMPARISON =========================
    echo
    output_loc="`pwd`/.container_mount/grade/results/results.json"
    python3 $2/tests/verify_out.py $1/expected.json $output_loc
    exit_code=$?
    echo
    echo ======================= END COMPARISON =======================
    echo 

    return $exit_code
}

run_test() { # $1 is variant_dir (the question/tests/ directory)

    # basically remove "run_test.sh" from the script call to get the directory
    script_dir=`pwd`

    prep_mount $1
    if [[ $? != "0" ]]; then return 1; fi
    echo done.

    echo Running the grader
    buildCont
    runImage

    if [[ $? == 0 ]]; then
        clean_up $cont
    else return 1; fi

    compare $1 $script_dir

    return $?
}

run_tests() {
    tests=`ls -d tests/*/`
    script_dir=`pwd`

    failures=0
    failed=""

    buildCont

    while IFS= read -r variant_dir; do
        
        echo Running test \"$variant_dir\"

        prep_mount $variant_dir
        if [[ $? != "0" ]]; then return 1; fi

        runImage
        if [[ $? != "0" ]]; then 
            failures=$((failures+1)); 
            failed="$failed\n$line"
        else
            compare $variant_dir $script_dir
            if [[ $? != "0" ]]; then 
                failures=$((failures+1)); 
                failed="$failed\n$line"
            fi
        fi

    done  <<< "$tests"

    echo -e "Failures: $failures $failed"
    return $((1 - ($failures == 0)))
}

new_test() {

    # make the base folders and files
    cd tests/
    mkdir $1
    mkdir $1/common
    mkdir $1/solution
    mkdir $1/var_case_one

    touch $1/solution/_submission_file

    # populate the json objects with filler
    meta_content="{\n    \"submission_file\": \"spec/my_spec.rb\",\n    \"submission_root\": \"\"\n}\n"
    expected_content="{\n    \"gradable\":true,\n    \"tests\":[],\n    \"score\":0.0\n}\n"
    data_content="{\n    \"submitted_answers\" : {\n        \"student-parsons-solution\": \"\"\n    },\n    \"raw_submitted_answers\" : {\n        \"student-parsons-solution\": \"\"\n    },\n    \"gradable\": true\n}\n"
    echo -e "$meta_content" >> $1/meta.json
    echo -e "$expected_content" >> $1/expected.json
    echo -e "$data_content" >> $1/data.json

    # return to base directory
    cd ../
    return
}

debug() {
    sudo docker run -it --rm --mount type=bind,source=`pwd`/.container_mount/grade,target=/grade --mount type=bind,source=`pwd`/debug_tools.sh,target=/tools.sh rspec-autograder:dev
    return
}

clean() {
    rm -rf .container_mount
    return
}