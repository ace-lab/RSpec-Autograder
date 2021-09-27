import os
from json import loads as json_loads

def make_dirs():
    # treat .testing/ as /grade/
    os.mkdir(".testing")
    os.mkdir(".testing/data")
    os.mkdir(".testing/results")
    os.mkdir(".testing/serverFilesCourse")
    os.mkdir(".testing/serverFilesCourse/suites")
    os.mkdir(".testing/student")
    os.mkdir(".testing/tests") # this should not be used
    os.mkdir(".testing/grader")

def load_test(suites_dir):
    # load the suites
    os.system(f"cp -r {suites_dir}/* .testing/serverFilesCourse/suites/")
    ## clean out the data.json, submission dir, and expected result
    ### data.json
    os.system("mv .testing/serverFilesCourse/suites/data.json .testing/data/")
    ### student files
    os.system(f"cp {suites_dir}/submission/* .testing/student/")
    #### we don't want _submission_file in student/
    os.system(f"rm .testing/student/_submission_file")
    #### nor do we want the submission dir already there, since writers shouldn't have to have it there
    os.system(f"rm -r .testing/serverFilesCourse/suites/submission")

def load_grader(source):
    os.system(f"cp {source}/* .testing/grader/")

def run_grader():
    os.system(f".testing/grader/run.py `pwd`/.testing")

def compareResult(test_dir):
    os.system(f"diff .testing/results/results.json {test_dir}/expected.json | less")
    # with open(".testing/results/results.json", 'r') as res:
    #     result_dict = json_loads(res.read())
    # with open(f"{test_dir}/expected.json", 'r') as exp:
    #     expected_dict = json_loads(exp.read())

for suites_dir in next(os.walk('./tests'))[1]:
    # set up the test
    make_dirs()
    load_test(suites_dir)
    load_grader("../grader")

    # run the system
    run_grader()

    # compare results
    result = compareResult(suites_dir)


    # clean up
    os.rmdir(".testing")



