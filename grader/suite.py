from typing import Dict, List

class Failure(object):
    def __init__(self, exception: str, err_msg: str, backtrace: List[str]) -> None:
        self.exception = exception
        self.err_msg = err_msg
        self.backtrace = backtrace

    def asdict(self) -> Dict[str, str]:
        return {
            'error_message' : self.err_msg,
            'exception' : self.exception
        }

    def __eq__(self, o) -> bool:
        same_ex = self.exception == o.exception
        
        return same_ex # and same_stack # maybe include stack ?

    def __repr__(self) -> str:
        return f"Failure({self.exception}: {self.err_msg})"

class Test(object):
    def __init__(self, id: str, desc: str, fail: Failure) -> None:
        self.id = id
        self.description = desc
        self.passed = fail is None
        self.failure = fail

    def __repr__(self) -> str:
        base = f"{self.id}: {self.description}"
        return base + ("pass" if self.passed else f"{self.failure}")

class Suite(object):
    def __init__(self, tests: Dict[str, Test], id: str) -> None:
        self.tests = tests
        self.id = id

    def __repr__(self) -> str:
        f"Suite({self.id},\n\t" + \
            '\n\t'.join([f"{test}" for test in self.tests]) + \
            '\n)'

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

            if ref.passed != sub.passed:
                fails.append({
                    'id' : testID,
                    'desc' : sub.description,
                    'reference' : "passed" if ref.passed else ref.failure.asdict(),
                    'submission' : "passed" if sub.passed else sub.failure.asdict()
                })
            else:
                score += 1

        return {
            'name' : f"Suite {reference.id}",
            'points' : score,
            'max_points' : len(reference.tests),
            'fails' : fails 
        }