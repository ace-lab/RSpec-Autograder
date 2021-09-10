from typing import Dict, List

class Failure(object):
    def __init__(self, err_msg: str, line_of_error: str) -> None:
        self.err_msg = err_msg
        self.line_of_error = line_of_error

class Test(object):
    def __init__(self, id: str, name: str, fail: Failure) -> None:
        self.id = id
        self.name = name
        self.passed = fail is None
        self.failure = fail

class Suite(object):
    def __init__(self, tests: List[Test], id: str) -> None:
        self.tests = tests
        self.id = id

    def grade(self) -> Dict:
        fails: List[Dict[str, str]] = []
        score: int = 0

        for test in self.tests:

            if not test.passed:
                fails.append({
                    'name' : test.name,
                    'line' : test.failure.line_of_error,
                    'err_msg' : test.failure.err_msg
                })
            else:
                score += 1

        return {
            'test_count' : len(self.tests),
            'score' : score,
            'fails' : fails 
        }