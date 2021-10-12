#!/bin/bash
mkdir $1
mkdir $1/common
mkdir $1/solution
mkdir $1/suite1
mkdir $1/submission

touch $1/solution/_submission_file
touch $1/submission/_submission_file
touch $1/meta.json
touch $1/data.json
touch $1/expected.json