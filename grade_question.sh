#!/bin/bash

# assuming $1 is the variants_dir (the question/tests/ directory)

which jq > /dev/null
if [[ $? != "0" ]]; then 
    echo "jq is required to run this script, please install and add it to your \$PATH"
fi

echo -n "Preparing mount files ... "

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
    exit 1
fi

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

exit $code
