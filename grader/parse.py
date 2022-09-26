from typing import Dict
from suite import Var, Test, Failure
from json import loads as json_loads
from json.decoder import JSONDecodeError

import pdb

# can use {work} for the working dir and {file} for ENTRY_FILE absolute path
GRADING_SCRIPT = "&&".join([
    'cd {work}',
    # 'bundle config path /grader/vendor/bundle',
    'bundle install --local --without production --quiet',
    'rspec --format json' 
])

ENTRY_FILE = ' ' # rspec will do everything for us, no need to specify a specific file
# alternative to this len is to have a delimeter that splits 
#   the test name into a test description and an ID
# ID_LEN = 4 # this is the length of each test id (e.g. 4 for '[12]', 3 for '124')

def verifyOutput(output: str) -> bool:
    """Returns if the passed string is a valid output"""
    try:
        data = json_loads(output)
    except JSONDecodeError:
        return False
    return data['summary']['errors_outside_of_examples_count'] == 0

def parseOutput(output: str, name: str) -> Var:
    """Function to parse the output of the GRADING_SCRIPT into a <Var> instance"""

    out = json_loads(output)
    
    parsed_tests: Dict[str, Test] = {}
    for rspec_test in out['examples']:
        test_id = rspec_test['full_description']#[-(ID_LEN):]
        # test_name = rspec_test['full_description'][:-(ID_LEN)]
        
        if rspec_test['status'] == 'passed':
            failure = None
        else:
            ex = rspec_test['exception']

            failure = Failure(
                exception=ex['class'], 
                err_msg=ex['message'], 
                backtrace=ex['backtrace']
            )

        test = Test(test_id, failure)

        parsed_tests[test_id] = test

    return Var(parsed_tests, name)