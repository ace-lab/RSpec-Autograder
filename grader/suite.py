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
    def __init__(self, desc: str, fail: Failure) -> None:
        # self.id = id
        self.description = desc
        self.passed = fail is None
        self.failure = fail

    def __repr__(self) -> str:
        base = f"{self.description}: {'passed' if self.passed else 'failed'}"
        return base #+ ("pass" if self.passed else f"{self.failure}")

class Var(object):
    def __init__(self, tests: Dict[str, Test], id: str) -> None:
        self.tests = tests
        self.id = id

    def __repr__(self) -> str:
        f"Var({self.id},\n\t" + \
            '\n\t'.join([f"{test}" for test in self.tests]) + \
            '\n)'

    def grade(self, reference) -> Dict:
        return Var.grade(self, reference)

    @classmethod
    def grade(cls, reference, submission) -> Dict:
        # fails: List[Dict[str, str]] = []
        # score: int = 0
        out = { }

        # msg = ""
        for testID in reference.tests.keys():
            ref: Test = reference.tests.get(testID)
            sub: Test = submission.tests.get(testID)

            out[testID] = {
                'correct' : False
            }
            
            # msg += f"`{ref.description}` : "

            if sub is None: 
                msg = "not found\n"
                import code
                code.interact()
            elif ref.passed != sub.passed:
                refRes = 'pass' if ref.passed else 'fail'
                subRes = 'pass' if sub.passed else 'fail'
                msg = f"should {refRes} but {subRes}ed\n"
                if ref.passed:
                    msg += sub.failure.err_msg + '\n'
            else:
                # when we fail as expected but don't fail due to an assertion
                if (not ref.passed) and (sub.failure.exception != ref.failure.exception):
                    msg = f"failed to unexpected error\n{sub.failure.err_msg}\n"
                    # if not, `continue`
                    continue
                msg = f"{'pass' if ref.passed else 'fail'}ed as intended\n"
                out[testID]['correct'] = True
            out[testID].update({
                "message" : msg,
                "supposed to pass" : ref.passed
            })

        return out
        # {
        #     'name' : reference.id,
        #     'points' : score,
        #     'max_points' : len(reference.tests),
        #     'message' : msg
        # }