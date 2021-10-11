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
mkdir .testing/data
mkdir .testing/results
mkdir .testing/serverFilesCourse
mkdir .testing/serverFilesCourse/suites
mkdir .testing/student
mkdir .testing/tests
mkdir .testing/grader

# load the suites
suite_dir="$(pwd)/$1/"
cp -r $suite_dir/* .testing/serverFilesCourse/suites
## clean out the data.json, submission dir, and expected result
### data.json
mv .testing/serverFilesCourse/suites/data.json .testing/data/
### student files
cp $suite_dir/submission/* .testing/student
#### we don't want _submission_file in student/
rm .testing/student/_submission_file
#### nor do we want the submission dir already there, since writers shouldn't have to have it there
rm -r .testing/serverFilesCourse/suites/submission

# load the expected results
cp $suite_dir/expected.json .testing

# load the grader
cp ../grader/* .testing/grader
chmod +x .testing/grader/run.py
# and run it
echo ==================== RUNNING THE GRADER ====================
echo
# only report errors
im="$(sudo docker build -q . | cut -d: -f2)"
echo image: $im
cont="$(sudo docker run -d $im /grader/run.py)"
echo container: $cont
echo container exited with code "$(sudo docker container wait $cont)"
sudo docker cp $cont:grade/results/results.json ./.testing/results/results.json
sudo docker container rm $cont > /dev/null
echo 
echo ========================= FINISHED =========================


# compare the result
echo ========================= DIFF RESULTS =========================
echo
diff .testing/results/results.json $suite_dir/expected.json
echo
echo =========================== END DIFF ===========================


# and clean up
rm -rf .testing