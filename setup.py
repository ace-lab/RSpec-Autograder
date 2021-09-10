#!/usr/bin/python3
import os
from re import match as re_match
from json import dumps as json_dumps
from typing import Dict, List
from suite import Suite

SUITES_DIR: str = 'suites'
SUITE_REGEX: str = '^suite[0-9]+$'
WORK_DIR: str = 'working'
GRADING_SCRIPT: str = '' 
assert GRADING_SCRIPT != '', 'You still need to define this'

def getSuites(dir: str = SUITES_DIR) -> List[str]:
    suites: List[str] = os.listdir(dir)
    suites = list(
        filter(
            lambda name: re_match(SUITE_REGEX),
            suites
        )
    )
    return suites

def prepareFiles(suite_name: str, workspace: str) -> None:
    os.system(f"rm {WORK_DIR}/*")
    os.system(f"cp {SUITES_DIR}/common/* {WORK_DIR}/")
    os.system(f"cp {SUITES_DIR}/{suite_name}/* {WORK_DIR}/")
    # TODO: define where the grader script will be and copy it in

def parseOutput(output: str) -> Suite:
    return None

if __name__ == '__main__':

    if not os.path.exists(WORK_DIR):
        os.mkdir(WORK_DIR)
    
    gradingData: Dict = {
        'gradable' : True,
        # this will store reports generated by <Suite>.grade()
        'tests' : []
    }

    for suite in getSuites("suites"):
        prepareFiles(suite=suite, workspace=WORK_DIR)

        output = os.popen(f"ruby {WORK_DIR}/{GRADING_SCRIPT}").readlines()
        suite = parseOutput(output)
        score_report = suite.grade()

        gradingData['tests'].append(score_report)
        
    with open('/grade/results/results.json', 'w') as results:
        json_data: str = json_dumps(gradingData)
        results.write(json_data)
