from typing import Dict
from suite import Suite, Test, Failure
from json import loads as json_loads

import pdb

# can use {work} for the working dir and {file} for ENTRY_FILE absolute path
GRADING_SCRIPT = 'cd {work} && bundle install --local > /dev/null && bundle exec rspec --format json' 
# GRADING_SCRIPT = 'su - autograder -c "pwd"'

ENTRY_FILE = ' ' # rspec will do everything for us, no need to specify a specific file
# alternative to this len is to have a delimeter that splits 
#   the test name into a test description and an ID
ID_LEN = 4 # this is the length of each test id (e.g. 4 for '[12]', 3 for '124')


def parseOutput(output: str, name: str) -> Suite:
    """Function to parse the output of the GRADING_SCRIPT into a <Suite> instance"""

    out = json_loads(output)
    
    parsed_tests: Dict[str, Test] = {}
    for rspec_test in out['examples']:
        test_id = rspec_test['full_description'][-(ID_LEN):]
        test_name = rspec_test['full_description'][:-(ID_LEN)]
        
        if rspec_test['status'] == 'passed':
            failure = None
        else:
            ex = rspec_test['exception']

            failure = Failure(
                exception=ex['class'], 
                err_msg=ex['message'], 
                backtrace=ex['backtrace']
            )

        test = Test(test_id, test_name, failure)

        parsed_tests[test_id] = test

    return Suite(parsed_tests, name)