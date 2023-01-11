build() { sudo docker build -t nalsoon/rspec-autograder . ; }
push() { sudo docker push nalsoon/rspec-autograder:latest ; }
buildPush() { build && push ; }

grade() {
    # assuming $1 is the variants_dir (the question/tests/ directory)

    which jq > /dev/null
    if [[ $? != "0" ]]; then 
        echo "jq is required to run this script, please install and add it to your \$PATH"
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
    cp -r $variant_dir/common .container_mount/grade/tests/
    cp -r $variant_dir/var_* .container_mount/grade/tests/
    cp -r $variant_dir/solution .container_mount/grade/tests/
    cp $variant_dir/meta.json .container_mount/grade/tests/

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
    bundle package --all --without-production --all-platforms
    bundle install --development
    cd $pd

    echo done.

    echo Running the grader
    # only report errors
    im="$(sudo docker build -q -t rspec-autograder:dev .  | cut -d: -f2)"
    echo \> Image name/hash: rspec-autograder:dev / $im
    cont="$(sudo docker run --network none --mount type=bind,source=`pwd`/.container_mount/grade,target=/grade -d $im /grader/run.py)"
    echo \> Container hash: $cont
    code="$(sudo docker container wait $cont)"
    echo \> Container exited with code $code

    if [[ $code == 0 ]]; then
        sudo chown -R $USER .container_mount/grade/
        # destroy the container
        echo -n Deleting continer ...
        sudo docker container rm $cont > /dev/null
        echo done.
    fi

    return $code
}

run_test() {
    # $1 is variant_dir

    # basically remove "run_test.sh" from the script call to get the directory
    script_dir=`pwd`

    # run the test 
    grade $1
    # stop if failed
    if [[ $? == "1" ]]; then return; fi

    # compare the result
    echo ========================= COMPARISON =========================
    echo
    output_loc="`pwd`/.container_mount/grade/results/results.json"
    python3 $script_dir/tests/verify_out.py $1/expected.json $output_loc
    echo
    echo ======================= END COMPARISON =======================

    return
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