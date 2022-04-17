from json import loads as json_loads
from sys import argv, exit

assert len(argv) > 1, "usage: verify_out.py <path/to/expected.json>"
exp_path = argv[1]

with open(exp_path, 'r') as f:
    exp = json_loads(f.read())

with open('.testing/grade/results/results.json') as f:
    res = json_loads(f.read())

res_parsed = {}
for test in res['tests']:
    res_parsed[test['name']] = test
exp_parsed = {}
for test in exp['tests']:
    exp_parsed[test['name']] = test

if exp_parsed == res_parsed:
    print(f"No difference found")
    exit()
else:
    r = set(res_parsed.items())
    e = set(exp_parsed.items())
    diff = e ^ r
    print(f"{len(diff)} differences found:")
    print(diff)


