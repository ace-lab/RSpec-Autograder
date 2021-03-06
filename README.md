# RSpec-Autograder

### TODO:
- (improvement) create an ergonomic way to make questions for this 
  - interface with existing parson's problem generation

## Quickstart:

To use, add the following to  `info.json`  in your question 
```json
"gradingMethod": "External",
"externalGradingOptions": {
        "enabled": true,
        "image" : "nasloon/rspec-autograder",
        "entrypoint": "/grader/run.py",
        "timeout" : 60
    }
```

Define a suite to be a version of the codebase that forms a complete program. This project uses "suites" to determine if a student submission is correct. 

A question writer, in their PrarieLearn question, must create 
- the folder `tests/` in the root directory of their question 
  - subfolder `tests/common/`
    - which will consist of the code that is shared between a majority of the suites
  - json file `tests/meta.json`
    - which will contain 
      - the mapping of `_submission_file` as a value for the key `"submission_file"`
      - (optional) the location to which additional submitted files would be copied
  - subfolder `tests/solution/`
    - which must contain the file `_submission_file` that has the instructor solution
  - a number of subfolders `tests/suite<number>`
    - each of which contains the difference from the files in `tests/common/` expressed by including a modified copy of the file that should be replaced/added to `tests/common/`

Thus, your `tests/` folder should contain something like this:
```
tests/
+-- common/
|   `-- replaced.rb
|
+-- solution/
|   +-- _submission_file  # this will hold the instructor's "submission"
|   |
|   ...                # any other files can be included*
|
+-- suite9001/
|   `-- replaced.rb    # this file will replace the one in common
|
`-- meta.json          # this will contain the aforementioned mappings
```
*The student would need to submit additional files in the file submission box on the right of each question, yet this feature has not yet been tested

## Grading Structure:

For each suite (consider `<suite_i>`) the following is done:
1) make an empty working directory (`working/`)
2) load the files from `tests/common/` into `working/`
3) load the files from `tests/<suite_i>/` into `working/`  
4) load the solution into `working/`
    - in which `_submission_file` will be appended to the file detailed in `meta.json`
    - and if `"submission_root"` is defined in `meta.json`, all files are copied to `working/<submission_root>`
5) run the `GRADING_SCRIPT` and serialize the output into `Suite` objects
    - `GRADING_SCRIPT` is defined in `grader/parse.py` and without source modification is   
      ```$ cd working/ && bundle install --quiet && rspec --format json```
6) repeat steps 1-3
7) load the student submission (which will be loaded into `suites/submission` upon launch of the image) into `working/`
    - the text input by the student will be in `tests/submission/_submission_file`
    - all other files will be in `tests/submission/`
8) repeat step 5
9)  compare the `Suite` object generated by the student's submission to that of the instructor's solution and report results to prairielearn

