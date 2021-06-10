# CSV Parser for different schema bank files
The code has been written and tested on python 3.9

### Folder Structure
Default bank import files folder ./bank_files
Default output folder is ./output

### Import logic. 
Parser will read the files in the  BANK_FILES_PATH folder one by one, and will
read them line by line, doing all the transformations/aggregations on a row level.
In case parser finds any error in a cell, it reports the whole line 
to the file configured in ERROR_FILE_PATH env var or in config_params.py.

### Launch
```buildoutcfg
1. cd test_task_banks_import
2. source ./set_env_vars.sh config.env
3. pip[3.9] install -r requirements.txt
4. python[3.9] main.py
```

### run tests
```
1.export PYTHONPATH='path to your folder'
2.pytest -s -v .
```

# Original Task

Dear Candidate,

Please go through below, Assignment Link, and create a Python Project for the same:
https://gist.github.com/Attumm/3927bfab39b32d401dc0a4ca8db995bd

Assignment Submission:
    • Create a GitHub Public link and submit the code. 
    • Share the URL – with recruitment team. 

Important Points:
    • Pythonicness of code is the most critical aspect, as the requirement to build a Python Application/Project.
    • Design & Code logic will be used to assess the Project. 
    • Code must be optimized with best data structures matching the programming requirements.
    • Code must be structured, and a runnable script.
    • Coding should be performed, keeping Testing criteria into account.
    • Do not use – Jupyter Notebook / Colab / Pandas
