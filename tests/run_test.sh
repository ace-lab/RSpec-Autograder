#!/bin/bash

# $1 is suites_dir

# make all the necessary dirs
mkdir .testing
mkdir .testing/data
mkdir .testing/results
mkdir .testing/serverFilesCourse
mkdir .testing/serverFilesCourse/suites
mkdir .testing/student
mkdir .testing/tests
mkdir .testing/grader

# load the suites
suite_dir="$(pwd)/$1/"
cp -r $suite_dir/* .testing/tests/
## clean out the data.json, submission dir, and expected result
### data.json
mv .testing/tests/data.json .testing/data/
### student files
cp $suite_dir/submission/* .testing/student
#### we don't want _submission_file in student/
# rm .testing/student/_submission_file
#### nor do we want the submission dir already there, since writers shouldn't have to have it there
# rm -r .testing/tests/submission

# load the expected results
cp $suite_dir/expected.json .testing

# load the grader
cp ../grader/* .testing/grader
chmod +x .testing/grader/run.py
# and run it
echo ===================== RUNNING THE GRADER =====================
echo
# only report errors
im="$(sudo docker build -q . | cut -d: -f2)"
echo \> Image hash: $im
cont="$(sudo docker run -d $im /grader/run.py)"
echo container: $cont
code="$(sudo docker container wait $cont)"
echo \> Container hash: $cont
echo \> Container exited with code "$(sudo docker container wait $cont)"
if [[ $code == "1" ]]; then
    echo ========================= FINISHED =========================
    exit
fi
sudo docker cp $cont:grade/results/results.json ./.testing/results/results.json
sudo docker container rm $cont > /dev/null
echo 
echo ========================== FINISHED ==========================


# compare the result
echo ========================= COMPARISON =========================
echo
python3 verify_out.py $suite_dir/expected.json
echo
echo ======================= END COMPARISON =======================

# cp bruh question1/expected.json
# cp .testing/results/results.json bruh


# and clean up
rm -rf .testing