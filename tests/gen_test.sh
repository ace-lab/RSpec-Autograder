#!/bin/bash
mkdir $1
mkdir $1/common
mkdir $1/solution
mkdir $1/var_case_one
mkdir $1/submission

touch $1/solution/_submission_file
# touch $1/submission/_submission_file
touch $1/data.json
touch $1/expected.json

echo -e "{\n    \"submission_file\": \"spec/my_spec.rb\"\n    \"submission_root\": \"\"}" >> $1/meta.json