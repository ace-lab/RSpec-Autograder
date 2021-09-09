import os
from re import match as re_match
from typing import List

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

def loadFiles(suite: str, workspace: str) -> None:
    os.system(f"cp {SUITES_DIR}/common/* {WORK_DIR}/")
    os.system(f"cp {SUITES_DIR}/{suite}/* {WORK_DIR}/")
    # TODO: define where the grader script will be and copy it in

if __name__ == '__main__':

    if not os.path.exists(WORK_DIR):
        os.mkdir(WORK_DIR)
    
    

    for suite in getSuites("suites"):
        loadFiles(suite=suite, workspace=WORK_DIR)
        output = os.system(f"ruby {WORK_DIR}/{GRADING_SCRIPT}")

# write_to("/grade/results/results.json", json.dumps(gradingData))
