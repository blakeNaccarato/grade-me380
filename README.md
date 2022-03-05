# Grade ME380

The scripts in this repo can be used to automate scoring of assignments. These scripts do not perform any "intelligent" actions such as detecting content or formatting issues, they simply keep track of points lost and allow for the grader to quickly insert "canned responses" for very common issues (e.g. "Wrong title page").

## Quick installation

- Clone this repo.
- Create a virtual environment in the root of the cloned repo and activate it in your IDE.
- Install the requirements in `requirements.txt`.
- Copy the YAML files from `examples` to the root of the cloned repo, or supply your own (names must match exactly).
- Copy the `.env` file from `examples` to the root of the cloned repo, or supply your own.
- Install AutoHotkey if you haven't already.

Now you should be able to launch the AutoHotkey scripts, which will attach the two most important scripts, `update_active_grade.py` and `toggle_review_pane.py` to keyboard shortcuts `Alt+W` and `Ctrl+Alt+W` respectively.

You can also run scripts directly in your IDE or from the command line. Other useful scripts are `open_all.py`, `save_all.py`, `close_all.py`, and `delete_all_comments.py`.

## In-depth tutorial

### Prerequisites

Make sure `Powershell 7`, `git`, and `python` are installed. These links should get you started:

- [Installing PowerShell](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.2#msi): Do select the boxes for "context menu" entries
- [Installing git](https://git-scm.com/downloads): Lots to customize, but don't bother customizing installation for now
- [Installing python](https://www.python.org/downloads/): No need to add to `$PATH`
- [Installing autohotkey](https://www.autohotkey.com/): Download current version

If you're not familiar with configuring these tools, just accept the default options when installing.

You may or may not need to reboot your computer after this. Then you should be able to find PowerShell 7 in your Start menu. By default it will start in your `$USER` folder, e.g. `C:/Users/You`. Performing the following step to clone a repo will therefore put that repo in that directory.

### Clone this repo

Clone this repo somewhere on your computer. For example, you could open a PowerShell prompt and type the following:

```pwsh
git clone https://github.com/blakeNaccarato/grade-me380.git grade-me380
cd grade-m380
```

This will clone the repo to your current working directory, and then navigate to that directory with `cd` (short for change directory). From here on out, whenever I say "root of the cloned repo", that refers to the folder that was just cloned and navigated to. It contains files like `README.md`, and a bunch of Python files, including `add_template_comments.py`.

### Ensure your PowerShell profile activates virtual environments in the CWD

The following snippet, if placed in your PowerShell profile, will run on startup of PowerShell prompts, and activate any virtual environments found in the current working directory:

```PowerShell
# If there is a Python virtual environment in the PWD, activate it
$PATH_VENV = ".\.venv\Scripts\Activate.ps1"
if (Test-Path $PATH_VENV) { & $PATH_VENV }
```

You can navigate to your PowerShell profile by typing the following in the PowerShell prompt:

```Powershell
notepad $PROFILE
```

Copying the snippet into your PowerShell profile and saving the file will ensure that a virtual environment in your current directory is activated whenever PowerShell is launched. This is needed for the AutoHotkey scripts to work properly.

### Create a virtual environment and activate it

Make sure that your PowerShell prompt is currently in the repo folder that you cloned (e.g. `C:/Users/You/grade-me380`). Then, enter the following:

```PowerShell
py -m venv .venv
```

Heads up, a quick way to open PowerShell in a folder is through the right-click context menu. You may need to reboot after installing PowerShell 7 for the first time if you don't see this.

![Open PowerShell here](/tutorial/4.png)

Open a PowerShell prompt in the root of the cloned repo and it should look like the following, with `(.venv)` at the start of the prompt. If it doesn't, then you didn't modify your PowerShell `$PROFILE` properly. Go back to that step and make sure the profile is properly set up.

![Activated virtual environment](/tutorial/5.png)

### Install requirements

In the PowerShell window with the green `(.venv)` prompt, enter the following:

```PowerShell
pip install -r requirements.txt
```

This will install the prerequisites to run the scripts in this repo.

### Download submissions

Download the submissions you want to grade.

![Download submissions](/tutorial/1.png)

### Extract submissions

Extract the submissions to a folder. Keep the default folder name `submissions`.

![Extract submissions](/tutorial/2.png)

### Move submissions folder into the root of the cloned repo

![Move submissions](/tutorial/3.png)

### Launch the autohotkey scripts

Double-click the scripts `hotkey_toggle_review_pane.ahk` and `hotkey_update_active_grade.ahk`. Note that these will bind the keyboard shortcut `Alt+W` to run the `update_active_grade.py` script, and  `Ctrl+Alt+W` to the `toggle_active_review_pane.py` script.

### General grading procedure (UNDER CONSTRUCTION)

This is my usual order of grading:

#### Add all template comments

Run `add_template_comments.py`. This adds template comments to all files in the `submissions` folder.

#### Open all reports

A useful script in this phase is `open_all.py`. Start by opening just one document, place it on your desktop where you want it to go, then run the script `open_all.py`. This will open all papers in the same position on your desktop.

#### Manually modify template comments if they are out of order

Template comments are added to the first occurrence of the expected headings. If students use the key words (such as "Introduction and Theory") before the first actual heading, then the comment will be inserted in the wrong place. Double-check each report and confirm that the template comments are on the headings. A common issue is if the student included a Table of Contents. You will have to move all comments down out of the table of contents and into the main body of the text.

Moving a comment entails selecting its contents, copying, inserting a comment where it should be, and pasting the contents. Then go back and delete the original comment.

#### Initially run the grader on all reports with `update_all_grades.py`

This will create a `grades.csv` in the same folder as the lab reports, summarizing the score that each student received for each section of their report, the total deductions they received, and their total grade for that report. Use this to check for fairness across reports.

#### Open a report and grade it

If you create a comment that starts with a lone number, like `4`, then the grader will take four points away from the section in which you put that comment, the next time it is run. You can hit `Enter` twice in such a comment block, and then describe why the student lost these points.

If you create a comment like `D4`, then the grader will make a four-point *deduction*, which is usually used for formatting errors. Content points are for things like missing figures, results, discussion, and so on. Deductions are subtracted from the overall report grade at the very end. You can hit `Enter` twice in such a comment block, and then describe why the student lost these points.

If you create a comment like `D4: G2`, then the grader will assess a four-point deduction, and also paste the contents of the deduction code `G2` in either `deductions_common.yaml` or `deductions_lab_specific.yaml` if it resides in the root of the repo. There are examples of these files in the `examples` folder of this repo. Be sure to copy them to the root of the repo, and modify as you see fit, in order to use this feature. This feature allows for common feedback to be duplicated exactly across reports.

Be careful about taking points off before the `"ABSTRACT: 10/10"` comment, because these points will not be tallied up. This may be fixed in the future, but for now, only make point-losing comments *after* the `"ABSTRACT: 10/10"` comment.

#### Update the grade of the report you're working on

When you're ready to update the grade of the report you're working on, run `update_grade.py`. You may also use the keyboard shortcut `Alt+W` if you have the Auto Hotkey script running.

#### When finished, remember to update all grades again

It is good practie to run `update_all_grades.py` once more after finishing grading. This will be sure that all reports have the latest grade total.

#### Close all documents

You can close all lab reports with `close_all.py`.
