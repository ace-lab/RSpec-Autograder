#!/bin/bash

# $1 is variant_dir

# basically remove "run_test.sh" from the script call to get the directory
script_dir="`pwd`/${0::-12}"

# run the test 
$script_dir/grade_question.sh $1
# stop if failed
if [[ $? == "1" ]]; then exit; fi

# compare the result
echo ========================= COMPARISON =========================
echo
output_loc="`pwd`/.container_mount/grade/results/results.json"
python3 $script_dir/tests/verify_out.py $1/expected.json $output_loc
echo
echo ======================= END COMPARISON =======================

# and clean up
rm -rf .container_mount