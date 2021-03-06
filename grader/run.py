#!/usr/bin/python3
import os
from sys import argv
from pprint import pformat, pprint
from re import match as re_match
from json import dumps as json_dumps
from json import loads as json_loads
from typing import Dict, Tuple
from suite import Var
from parse import parseOutput, verifyOutput, GRADING_SCRIPT, ENTRY_FILE

ROOT_DIR: str = '/grade' if len(argv) < 2 else argv[1]

VARS_DIR: str = f"{ROOT_DIR}/tests"
SOLUTION_DIR: str = f"{VARS_DIR}/solution"
SUBMISSION_DIR: str = f"{VARS_DIR}/submission"

VAR_REGEX: str = '^var_.+$'
# this will be made when this script is run
WORK_DIR: str = f"{ROOT_DIR}/working"

# this can be defined properly in `parse.py`
GRADING_SCRIPT: str = GRADING_SCRIPT.format(work=WORK_DIR, file=f"{WORK_DIR}/{ENTRY_FILE}")

assert os.path.exists(f"{ROOT_DIR}"), f"ERROR: {ROOT_DIR} not found! Mounting may have failed."

with open(f"{VARS_DIR}/meta.json", 'r') as info:
    grading_info = json_loads(info.read())
with open(f"{ROOT_DIR}/data/data.json", 'r') as data:
    content = data.read()
    # print(content)
    submission_data = json_loads(content)

def lsVars(dir: str = VARS_DIR):
    """get the folder names that match VAR_REGEX"""
    yield from filter(
        lambda name: re_match(VAR_REGEX, name),
        os.listdir(dir)
    )

def load_var(var_name: str, solution: bool) -> Var:
    """Empties the working directory, copies in the necessary files from common/, the variant, and the submission"""
    # nuke working directory
    os.system(f"rm -rf {WORK_DIR}/*")
    # copy common files
    os.system(f"cp -r {VARS_DIR}/common/* {WORK_DIR}")
    # copy in files from the variant
    os.system(f"cp -r {VARS_DIR}/{var_name}/* {WORK_DIR}")

    # copy the submitted files
    if solution:
        sub_dir = SOLUTION_DIR
    else:
        sub_dir = SUBMISSION_DIR

    ## append the submitted code snippet
    os.system(f"cat {sub_dir}/_submission_file >> {WORK_DIR}/{grading_info['submission_file']}")
    ## and all additionally submitted files
    if 'submission_root' in grading_info.keys():
        os.system(f"cp {sub_dir}/* {WORK_DIR}/{grading_info['submission_root']}/")
    ## but we accidentally copy in the submission again, so let's remove that
    os.system(f"rm {WORK_DIR}/{grading_info['submission_root']}/_submission_file")

def runVar(var_name: str, solution: bool) -> Tuple[Var, str]:
    """Prepares, runs, and parses the execution of a variant from its name (its folder)"""
    load_var(var_name=var_name, solution=solution)
    output = os.popen(f"cd {WORK_DIR} && {GRADING_SCRIPT}").read()
    if not verifyOutput(output):
        suite = "instructor" if solution else "student"
        print(f"Error when running variant {var_name} on {suite} suite. Output:")
        print(f"> {output}")
        exit(1)
    # print(f"OUT: {output}")
    vname = var_name[len("var_"):] # cut out the "var_" at the front
    vname = vname.capitalize() # fix capitalization ("hello_There" -> "Hello_there")
    vname = vname.replace("_", " ")
    return parseOutput(output=output, name=vname), output

if __name__ == '__main__':
    
    gradingData: Dict = {
        'gradable' : True,
        # this will store reports generated by Var.grade()
        'tests' : []
    }

    if not os.path.exists(WORK_DIR):
        os.mkdir(WORK_DIR)

    if not os.path.exists(SUBMISSION_DIR):
        os.mkdir(SUBMISSION_DIR)
    # there may not be files in student/, so we just hide the error
    # TODO: check if files exist before doing this
    os.system(f"cp {ROOT_DIR}/student/* {SUBMISSION_DIR} 2> /dev/null")
    
    # copy student submission from /grade/data/data.json 
    #   into the end of f"{SUBMISSION_DIR}/_submission_file"
    with open(f"{SUBMISSION_DIR}/_submission_file", 'w') as sub:
        sub.write(
            submission_data['submitted_answers']['student-parsons-solution']
        )

    pts = 0
    max_pts = 0
    out = { }
    # if False:
    vars = lsVars()
    var = next(vars)
    ref_var, ref_out = runVar(var_name=var, solution=True)
    sub_var, sub_out = runVar(var_name=var, solution=False)

    report = Var.grade(ref_var, sub_var)
    for testID, data in report.items():
        out[testID] = {
            'message' : f"{ref_var.id} : {data['message']}",
            'points' : data['correct'],
            'max_points' : 1
        }
        

    for var in vars:
        ref_var, ref_out = runVar(var_name=var, solution=True)
        sub_var, sub_out = runVar(var_name=var, solution=False)

        report = Var.grade(ref_var, sub_var)

        for testID, data in report.items():
            out[testID]['message'] += f"{ref_var.id} : {data['message']}"
            out[testID]['points'] += int(data['correct'])
            out[testID]['max_points'] += 1

    gradingData['tests'] = [ 
        {
            "name" : testID,
            "output" : data['message'],
            "points" : data['points'],
            "max_points" : data['max_points']
        }
        for testID, data in out.items()
    ]

    pts = sum([ test['points'] for test in gradingData['tests'] ])
    max_pts = sum([ test['max_points'] for test in gradingData['tests'] ])
    gradingData['score'] = pts / max_pts

    if not os.path.exists(out_path := f"{ROOT_DIR}/results"):
        os.mkdir(out_path)
    with open(f'{ROOT_DIR}/results/results.json', 'w+') as results:
        json_data: str = json_dumps(gradingData)
        pprint(gradingData)
        results.write(json_data)
