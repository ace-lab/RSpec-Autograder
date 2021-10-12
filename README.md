# RSpec-Autograder

### TODO:
- (requirement) interface with existing parson's problem generation
- (improvement) create an ergonomic way to make questions for this 

To use, add the following to  `info.json`  in your question 
```json
"externalGradingOptions": {
        "enabled": true,
        "image" : TO BE DETERMINED,
        "serverFilesCourse": ["suites/"],
        "entrypoint": "/grade/setup.py",
        "timeout" : 60
    }
```

Define a suite to be a version of the codebase that forms a complete program. This project uses "suites" to determine if a student submission is correct. 

A question writer, in their PrarieLearn question, must create the folder `suites/` in the root directory of their question with the subfolders `suites/common/` and `suites/solution/` along with the json file `suites/meta.json`. Each suite's difference from the files in `suites/common/` can be expressed in a folder `suites/suite<number>/` by including a modified copy of the file that should be replaced/added to `suites/common/`.

Thus, your directory structure should look like this:
```
suites/
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
*The student would need to submit additional files in the file submission box on the right of each question

For each suite (consider `<suite_i>`) the following is done:
1) make an empty working directory (`working/`)
2) load the files from `suites/common/` into `working/`
3) load the files from `suites/<suite_i>/` into `working/`  
4) load the solution into `working/`
    - all files will be copied as-is
    - excepting `_submission_file`, which will be appended to the file detailed in `meta.json`
5) run the `GRADING_SCRIPT` and serialize the output into `Suite` objects
6) repeat steps 1-4
7) load the student submission (which will be loaded into `suites/submission` upon launch of the image) into `working/`
    - the text input by the student will be in `suites/submission/_submission_file`
    - all other files will be in `suites/submission/`
8) repeat step 5
9) compare the `Suite` object generated by the student's submission to that of the instructor's solution

All of these comparisons are then serialized and sent back to the Prarielearn instance that then shows the student their feedback.  
