#!/bin/bash

# $1 is suites_dir

# sudo apt update
# sudo apt install -y rbenv
# eval "$(rbenv init -)"
# mkdir -p "$(rbenv root)"/plugins
# git clone https://github.com/rbenv/ruby-build.git "$(rbenv root)"/plugins/ruby-build
# echo The following install may take up to 30 mins, feel free to grab a coffe
# rbenv install 2.7.1
# rbenv rehash
# gem install bundle

# make all the necessary dirs
mkdir .testing

mkdir .testing/grade
mkdir .testing/grade/data
mkdir .testing/grade/serverFilesCourse
mkdir .testing/grade/student
mkdir .testing/grade/tests

mkdir .testing/results

# load the variants
variant_dir="$(pwd)/$1/"
cp -r $variant_dir/* .testing/grade/tests/
## clean out the data.json, submission dir, and expected result
### data.json
mv .testing/grade/tests/data.json .testing/grade/data/
### student files
if [[ -d $variant_dir/submission ]]; then
    cp $variant_dir/submission/* .testing/grade/student
    #### we don't want _submission_file in student/
    rm .testing/grade/student/_submission_file
    #### nor do we want the submission dir already there, since writers shouldn't have to have it there
    rm -r .testing/grade/tests/submission
fi
### expected result
rm .testing/grade/tests/expected.json

# load the expected results
cp $variant_dir/expected.json .testing

# run it
echo ==================== RUNNING THE GRADER ====================
echo
# only report errors
im="$(sudo docker build -q .. | cut -d: -f2)"
echo image: $im
cont="$(sudo docker run --mount type=bind,source=`pwd`/.testing/grade,target=/grade -d $im /grader/run.py)"
echo container: $cont
code="$(sudo docker container wait $cont)"
echo container exited with code $code
if [[ $code == "1" ]]; then
    echo ========================= FINISHED =========================
    exit
fi
sudo docker cp $cont:grade/results/results.json ./.testing/results/results.json
sudo docker container rm $cont > /dev/null
echo 
echo ========================= FINISHED =========================


# compare the result
echo ========================= COMPARISON =========================
echo
python3 verify_out.py $suite_dir/expected.json
echo
echo =========================== END COMPARISON ===========================

# cp bruh question1/expected.json
# cp .testing/results/results.json bruh


# and clean up
rm -rf .testing