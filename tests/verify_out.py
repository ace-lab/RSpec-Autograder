from json import loads as json_loads
from sys import argv, exit
from typing import Dict

assert len(argv) > 2, "usage: verify_out.py <path/to/expected.json> <path/to/produced.json>"
exp_path = argv[1]
res_path = argv[2]

class PLTest:
    
    def __init__(self, name: str, output:str, points:int, max_points:int = 1):
        self.name = name
        self.output = output
        self.points = points
        self.max_points = max_points
    
    def __eq__(self, other) -> bool:
        same_name = self.name == other.name
        similar_out = set(self.output.split('\n')) == set(other.output.split('\n'))
        same_points = self.points == other.points
        same_max_points = self.max_points == other.max_points

        return same_name and same_points and same_max_points and similar_out

def parse_json(path: str) -> Dict[str, PLTest]:
    
    parsed: Dict[str, PLTest] = {}

    with open(path, 'r') as f:
        data: Dict = json_loads(f.read())
        for test in data['tests']:
            parsed[test['name']] = PLTest(**test)
    
    return parsed

res_parsed: Dict[str, PLTest] = parse_json(res_path)
exp_parsed: Dict[str, PLTest] = parse_json(exp_path)

if exp_parsed == res_parsed:
    print(f"No difference found")
    exit()
else:
    expected = []
    unexpected = []
    different = []
    for test, grades in exp_parsed.items():
        if test not in res_parsed.items():
            expected.append((test, grades))
        elif res_parsed[test] != grades:
            different.append(test)

    for test, grades in res_parsed.items():
        if test not in exp_parsed.items():
            unexpected.append((test, grades))
    print(f"{len(expected)} expected tests not found")
    print(f"{len(unexpected)} unexpected tests found")
    print(f"{len(different)} differing grades found")
    print("Run with python -i to inspect `expected`, `unexpected`, and `different`")
    if (len(unexpected) + len(different)) > 0:
        exit(1)


