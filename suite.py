from setup import prepareFiles
from typing import Dict, List

class Failure(object):
    def __init__(self, err_msg: str, line_of_error: str) -> None:
        self.err_msg = err_msg
        self.line_of_error = line_of_error

    def asdict(self) -> Dict[str, str]:
        return {
            'error_message' : self.err_msg,
            'line_of_error' : self.line_of_error
        }

    def __eq__(self, o) -> bool:
        same_line = self.line_of_error == o.line_of_error

        return same_line # and same_stack # maybe include stack ?

class Test(object):
    def __init__(self, id: str, name: str, fail: Failure) -> None:
        self.id = id
        self.name = name
        self.passed = fail is None
        self.failure = fail

class Suite(object):
    def __init__(self, tests: Dict[str, Test], id: str) -> None:
        self.tests = tests
        self.id = id

    def grade(self, reference) -> Dict:
        return Suite.grade(self, reference)

    @classmethod
    def grade(cls, reference, submission) -> Dict:
        fails: List[Dict[str, str]] = []
        score: int = 0

        for testID in reference.tests.keys():
            ref: Test = reference.get(testID)
            sub: Test = submission.get(testID)

            if sub is None:
                raise ValueError(f"Submission does not contain graded test [{testID}]")

            if ref.failure != sub.failure:
                fails.append({
                    'id' : testID,
                    'reference' : ref.failure.asdict(),
                    'submission' : sub.failure.asdict()
                })
            else:
                score += 1

        return {
            'name' : f"Suite {reference.id}",
            'points' : score,
            'max_points' : len(reference.tests),
            'fails' : fails 
        }