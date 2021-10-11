from typing import Dict, List

class Failure(object):
    def __init__(self, exception: str, err_msg: str, backtrace: List[str]) -> None:
        self.exception = exception
        self.err_msg = err_msg
        self.backtrace = backtrace

    def asdict(self) -> Dict[str, str]:
        return {
            'error_message' : self.err_msg,
            'line_of_error' : self.line_of_error
        }

    def __eq__(self, o) -> bool:
        same_ex = self.exception == o.exception
        
        return same_ex # and same_stack # maybe include stack ?

class Test(object):
    def __init__(self, id: str, desc: str, fail: Failure) -> None:
        self.id = id
        self.description = desc
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

        # assert False, f"ref: {reference.tests} \n\n\nsub: {submission.tests}"

        for testID in reference.tests.keys():
            ref: Test = reference.tests.get(testID)
            sub: Test = submission.tests.get(testID)

            if sub is None:
                raise ValueError(f"Submission does not contain graded test [{testID}]")

            if ref.failure != sub.failure:
                fails.append({
                    'id' : testID,
                    'desc' : sub.description,
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