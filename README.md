# RSpec-Autograder

### TODO:
- (improvement) add variable file extension support

To use, add the following to  `info.json`  in your question 
```json
"exernalGradingOptions": {
        "enabled": true,
        "serverFilesCourse": ["suites/"],
        "entrypoint": "/grade/setup.py",
        "timeout" : 60
    }
```

Define a suite to be a version of the codebase that forms a complete program. This project uses "suites" to determine if a student submission is correct. 

A question writer, in their PrarieLearn question, must create the folder `suites/` in the root directory of their question with the subfolders `suites/common/` and `suites/solution/`. Each suite's difference from the files in `suites/common/` can be expressed in a folder `suites/suite<number>/` by including a modified copy of the file that should be replaced/added to `suites/common/`. In addition, you should have an entry point called `suites/common/entry` that `GRADING_SCRIPT` will be run on. 

Thus, your directory structure should look like this:
```
suites/
+-- common/
|   +-- entry.rb
|   `-- replaced.rb
|
+-- solution/
|   +-- submission.rb  # this will hold the instructor's "submission"
|   |
|   ...                # any other files can be included*
|
+-- suite9001/
    `-- replaced.rb    # this file will replace the one in common
```
*The student would have to submit additional files in the file submission box on the right of each question

Each suite (consider `<suite_i>`) will be run as follows:
- make an empty working directory (`working/`)
- load the files from `suites/common/` into `working/`
- load the files from `suites/<suite_i>/` into `working/`  
[//]: <> (TODO: include how student files and the actual parson problem will be loaded)  
- load the student submission into `working/` 
- run `GRADING_SCRIPT` passed the `working/entry` file 
- compare the output test cases with those of the instructor's solution