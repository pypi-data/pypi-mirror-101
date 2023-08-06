MaRChE
======

**MA**ssive **R**epository **CH**anges for **E**veryone
-------------------------------------------------------

MaRChE is an addons based software created to apply recursive changes on a lot of repositories with only one (reusable) script and one (reusable) configuration file.

# Installation

Use virtualenv to separate MaRChE environment from system one.

```
$ git clone git@github.com:openforceit/marche.git
$ cd marche
$ virtualenv -p python3 venv
$ source venv/bin/activate
(venv)$ python3 -m pip install -r requirements.txt
```

# Usage

## Get scripts list

`(venv)$ python3 marche.py available-scripts`

A list of scripts (folders in `scripts` path) will be showed.

Every folder is callable as a script.

## Call script

```
(venv)$ python3 marche.py script
    -t TOKEN
    [--bar/--no-bar]
    [--collect-pr/--no-collect-pr]
    SCRIPT_NAME
    [--] [<script_options>]
```

`SCRIPT_NAME` is the script name that user can get from `available-scripts`

`TOKEN` is a Github developer token that can be generated here: https://github.com/settings/tokens.

`--bar/--no-bar` Show or hide progress bar. Default value show the bar.

`--collect-pr/--no-collect-pr` Show or hide all the Pull Requests created by MaRChE. Default value show the collected pr.

`script_options` is a list of POSIX-style, whitespace-separated arguments that are passed to the script. These arguments may or may not be required depending on the script itself. Check the script documentation for more details.

# How to dev an addon

MaRChE addons must be created in `scripts` path.

A MaRChE addons is composed by 2 mandatory files and 1 folder (not mandatory):

```
addon_name
| - marche.py
| - marche.yaml
| - resources
```

## Resources

Is the folder where MaRChE search for all external files. If you need to read a txt file or an image, put them in this folder and use `read_local_file` function of `repo`.

## Marche.yaml

It's a YAML file. Every marche.yaml must contains keys called version and repo. Others keys are not required.

### **`version`** [required]

Version of marche.yaml structure. It's used for retrocompatibility.

### **`repo`** [required]

List of repositories information:

#### **`name`**

The repo name composed by *ORGANIZATION/REPO_NAME*

#### **`source_branch`**

The branch used as source

#### **`target_branch`**

The branch used as target. If it doesn't exist, will be created.

### **`comments`**

Comments relative to script

## Marche.py

It's a python script. Every marche.py must contains a function called `marche`.

```
def marche(repo, *args, **kwargs):
    ....
```

`repo` is a required argument used to access to repo object.

### Repo object

#### **Attributes**

##### **`repo`**

Reference to repo object from Github module (https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html).

All the methods available for this object can be found here: https://pygithub.readthedocs.io/en/latest/index.html

##### **`name`**

Repository name get from configuration file.

##### **`source_branch`**

Name of the branch used as base to generate PR.

##### **`target_branch`**

Name of the branch used as target to generate PR. If it doens't exist, will be created.

##### **`collect_pr`**

Property to manage a collection of new pull requests of every repo

#### **Functions**

##### **`branch_exists(name)`**

Return branch object, relative to branch name, if it exists or return False.

```
    if repo.branch_exists('test'):
        print('Test is here!')
    else:
        print('Create test branch')
```

##### **`create_file(file_name, file_content, commit_message)`**

Create a new file on target branch. A new commit will be generated.
Return a commit object.

```
    commit = repo.create_file(
        'marche.txt', 'Sample file', '[ADD] Marche txt')
    print(commit)
```

##### **`update_file(file_name, file_content, commit_message)`**

Update an existing file on target branch. A new commit will be generated.
Return a commit object.

```
    commit = repo.update_file(
        'marche.txt', 'Sample file with MaRChE', '[ADD] Marche txt')
    print(commit)
```

##### **`delete_file(file_name, commit_message)`**

Delete an existing file on target branch. A new commit will be generated.
Return a commit object.

```
    commit = repo.delete_file(
        'marche.txt', '[REM] Marche txt')
    print(commit)
```

##### **`read_file(file_name)`**

Read an existing file content from source branch. Return a bytes object.

```
    content = repo.read_file('.gitignore')
    print(content)
    print(content.replace(b'DS_Store', b'XXXXXXXXXXXX'))
```

##### **`read_local_file(file_name)`**

Read an existing file content from `resources` local path. Return a bytes object.

```
    content = repo.read_local_file('gitignore_template')
    print(content)
```

##### **`create_pr(title, body, reviewers)`**

Create a new PR from target branch to source branch. Return a pr object. `reviewers` is an optional list of github handles to add as reviewers of the PR.

```
    pr = repo.create_pr('Test PR', 'MaRChE Rulez!')
    print(pr)
```

##### **`collected_pr()`**

Show list of new pull requests created by MaRChE

```
    pr = repo.create_pr('Test PR', 'MaRChE Rulez!')
    print(repo.collected_pr())
```

##### **`log_info(message)`**

Show an info message on log default system

```
    repo.log_info('Hello World!')
```

##### **`log_warning(message)`**

Show a warning message (red text) on log default system

```
    repo.log_warning('OPS: Server is on fire!')
```

##### **`log_debug(message)`**

Show a debug message (orange text) on log default system

```
    repo.log_debug('This is the bug!')
```

##### **`log_ok(message)`**

Show a success message (green text) on log default system

```
    repo.log_ok('MaRChE is cool!')
```
