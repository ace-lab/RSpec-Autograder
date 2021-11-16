from json import loads as json_loads
from sys import argv, exit

exp_path = argv[1]

with open(exp_path, 'r') as f:
    exp = json_loads(f.read())

with open('.testing/results/results.json') as f:
    res = json_loads(f.read())

res_parsed = {}
for suite in res['tests']:
    res_parsed[suite['name']] = suite
    res_parsed[suite['name']].pop('reference_output')
    res_parsed[suite['name']].pop('submission_output')


exp_parsed = {}
for suite in exp['tests']:
    exp_parsed[suite['name']] = suite
    exp_parsed[suite['name']].pop('reference_output')
    exp_parsed[suite['name']].pop('submission_output')

if exp_parsed == res_parsed:
    print(f"No difference found")
    exit()
else:
    r = set(res_parsed.items())
    e = set(exp_parsed.items())
    diff = e ^ r
    print(f"{len(diff)} differences found:")
    print(diff)


