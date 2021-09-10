
class Test(object):
    def __init__(self, id: str, name: str, passed: bool, err_msg: str, line_of_error: str) -> None:
        self.id = id
        self.name = name
        self.passed = passed
        self.err_msg = line_of_error
        self.line_of_error = line_of_error
