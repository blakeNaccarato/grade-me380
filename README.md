# Grade ME380

The scripts in this repo can be used to automate the scoring of ME380 lab reports. These scripts do not perform any "intelligent" actions such as detecting content or formatting issues, they simply keep track of lab report scores, update a CSV of grades for that report, and allow for the grader to quickly insert "canned responses" for very common issues.

<!-- markdownlint-disable no-emphasis-as-heading -->
**Table of Contents**
<!-- markdownlint-restore-->


- [Summary of scripts](#summary-of-scripts)
- [Installation](#installation)
  - [Quick setup](#quick-setup)
  - [In-depth installation](#in-depth-installation)
    - [Prerequisites](#prerequisites)
    - [Clone this repo](#clone-this-repo)
    - [Ensure your PowerShell profile activates virtual environments in the CWD](#ensure-your-powershell-profile-activates-virtual-environments-in-the-cwd)
    - [Create a virtual environment and activate it](#create-a-virtual-environment-and-activate-it)
    - [Install the requirements](#install-the-requirements)
- [Usage](#usage)
  - [Download, extract, and move student submissions](#download-extract-and-move-student-submissions)
  - [Launch the AutoHotkey scripts](#launch-the-autohotkey-scripts)
  - [Add all template comments](#add-all-template-comments)
  - [Open all reports](#open-all-reports)
  - [Manually modify incorrect template comments](#manually-modify-incorrect-template-comments)
  - [Initially run the grader on all reports](#initially-run-the-grader-on-all-reports)
  - [Start grading reports](#start-grading-reports)
  - [Update the grade of the active report](#update-the-grade-of-the-active-report)
  - [Update all grades again when finished](#update-all-grades-again-when-finished)
- [Workaround in case a certain script isn't working](#workaround-in-case-a-certain-script-isnt-working)

## Summary of scripts

Here is a quick overview of each of the scripts and what they do.

- `add_template_comments.py`: Adds template comments to all submissions.
- `close_all.py`: Saves and closes all submissions.
- `deductions_to_semicolon_separated_variables.py`: Writes `common_deductions.yaml` to a semicolon-separated-variables file, `deductions.csv`.
- `deductions.py`: Not meant to be run directly. Holds the list of deduction code lists to search through.
- `delete_all_comments.py`: Deletes all comments from all submissions. Be careful with this one.
- `save_all.py`: Save all submissions without closing them.
- `shared.py`: Not meant to be run directly. Shared constants used by other scripts. Template comment insertion and grading behavior can be customized if you modify this.
- `toggle_active_review_pane.py`: Opens the review pane sidebar for the active submission. Useful for quickly navigating comments.
- `update_active_grade.py`: Updates the grade of the active submission.
- `update_all_grades.py`: Updates the grades of all submissions.


## Installation

### Quick setup

- Clone this repo.
- Create a virtual environment in the root of the cloned repo and activate it in your IDE.
- Install the requirements in `requirements.txt`.
- Copy the YAML files from `examples` to the root of the cloned repo, or supply your own (names must match exactly).
- Copy the `.env` file from `examples` to the root of the cloned repo, or supply your own.
- Install AutoHotkey if you haven't already.

Now you should be able to launch the AutoHotkey scripts, which will attach the two most important scripts, `update_active_grade.py` and `toggle_review_pane.py` to keyboard shortcuts `Alt+W` and `Ctrl+Alt+W` respectively.

You can also run scripts directly in your IDE or from the command line. Other useful scripts are `open_all.py`, `save_all.py`, `close_all.py`, and `delete_all_comments.py`.

### In-depth installation

#### Prerequisites

Make sure `Powershell 7`, `git`, and `python` are installed. These links should get you started:

- [Installing PowerShell](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.2#msi): Do select the boxes for "context menu" entries
- [Installing git](https://git-scm.com/downloads): Lots to customize, but don't bother customizing installation for now
- [Installing python](https://www.python.org/downloads/): No need to add to `$PATH`
- [Installing AutoHotkey](https://www.autohotkey.com/): Install the "current version"

If you're not familiar with configuring these tools, just accept the default options when installing.

You may or may not need to reboot your computer after this. Then you should be able to find PowerShell 7 in your Start menu. By default it will start in your `$USER` folder, e.g. `C:/Users/You`. Performing the following step to clone a repo will therefore put that repo in that directory.

#### Clone this repo

Clone this repo somewhere on your computer. For example, you could open a PowerShell prompt and type the following:

```pwsh
git clone https://github.com/blakeNaccarato/grade-me380.git grade-me380
cd grade-m380
```

This will clone the repo to your current working directory, and then navigate to that directory with `cd` (short for change directory). From here on out, whenever I say "root of the cloned repo", that refers to the folder that was just cloned and navigated to. It contains files like `README.md`, and a bunch of Python files, including `add_template_comments.py`.

#### Ensure your PowerShell profile activates virtual environments in the CWD

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

#### Create a virtual environment and activate it

Make sure that your PowerShell prompt is currently in the repo folder that you cloned (e.g. `C:/Users/You/grade-me380`). Then, enter the following:

```PowerShell
py -m venv .venv
```

Heads up, a quick way to open PowerShell in a folder is through the right-click context menu. You may need to reboot after installing PowerShell 7 for the first time if you don't see this.

![Open PowerShell here](/tutorial/4.png)

Open a PowerShell prompt in the root of the cloned repo and it should look like the following, with `(.venv)` at the start of the prompt. If it doesn't, then you didn't modify your PowerShell `$PROFILE` properly. Go back to that step and make sure the profile is properly set up.

![Activated virtual environment](/tutorial/5.png)

#### Install the requirements

In the PowerShell window with the green `(.venv)` prompt, enter the following:

```PowerShell
pip install -r requirements.txt
```

This will install the prerequisites to run the scripts in this repo.

## Usage

This is my particular workflow for using these scripts. You may find your own workflow, or choose to modify some of the scripts as you see fit. This particular usage tutorial assumes that you have a folder named `submissions` in the root of the cloned repo.

If you're comfortable using environment variables, you can specify a different folder to look for by setting the environment variable `DOCX_DIRECTORY`. If you would like the gradebook to be named something else, you may set the environment variable `GRADEBOOK_NAME` as well. Eventually I want to replace this environment variable based configuration with Dynaconf configuration.

### Download, extract, and move student submissions

Download the submissions you want to grade.

![Download submissions](/tutorial/1.png)

Extract the submissions to a folder. Keep the default folder name `submissions`.

![Extract submissions](/tutorial/2.png)

Move submissions into the root of the cloned repo.

![Move submissions](/tutorial/3.png)

### Launch the AutoHotkey scripts

Double-click the scripts `hotkey_toggle_review_pane.ahk` and `hotkey_update_active_grade.ahk`. Note that these will bind the keyboard shortcut `Alt+W` to run the `update_active_grade.py` script, and  `Ctrl+Alt+W` to the `toggle_active_review_pane.py` script.

### Add all template comments

Run `add_template_comments.py`. This adds template comments to all files in the `submissions` folder. Template comments are added to the first occurrence of the expected headings, such as "Abstract", "Introduction and Theory", and so on. The number of content points earned in that section is also shown, starting at the maximum possible number of points. Running the grader on a given document will search the document for your comments containing points marked off, and modify these template comments accordingly. A total lab report score comment is also added to the top of the document, which also shows the total deductions (e.g. formatting points lost).

### Open all reports

Start by opening just one document, place it on your desktop where you want it the other reports to open up in as well, then run the script `open_all.py`. This will open all papers in the same position on your desktop.

### Manually modify incorrect template comments

If students use the key words (such as "Introduction and Theory") before the heading of the same name, then the comment will be inserted in the wrong place. Double-check each report and confirm that the template comments are on the headings. A common issue is if the student included a Table of Contents. You will have to move all comments down out of the table of contents and into the main body of the text.

Moving a comment entails selecting its contents, copying it, inserting a comment in the proper place, pasting the contents, then deleting the original comment. Do this for each incorrectly-placed template comment in each report.

### Initially run the grader on all reports

Once you have ensured that all template comments are in the right place, run `update_all_grades.py`. This will create a `grades.csv` in the same folder as the lab reports, summarizing the score that each student received for each section of their report, the total deductions they received, and their total grade for that report. Use this to check for fairness across reports. If you wish, you can create an XLSX file that ingests `grades.csv` into a table for more sophisticated operations on the grades.

### Start grading reports

At any time you can invoke the grader on the currently active Word document by running `update_grade.py` or by pressing the AutoHotkey shortcut `Alt+W`. The points you take off while grading reports will not be tallied up until you run the grader. Running the grader multiple times will simply update the scores in the document.

If you create a comment that starts with a lone number, like "4", then the grader will take four points away from the section in which you put that comment, the next time it is run. You can hit `Enter` twice in such a comment block, and then describe why the student lost these points.

![Content points lost](/tutorial/8.png)

If you create a comment like "D2", then the grader will make a two-point *deduction*, which is usually used for formatting errors. Content points are for things like missing figures, results, discussion, and so on. Deductions are subtracted from the overall report grade at the very end. You can hit `Enter` twice in such a comment block, and then describe why the student lost these points. For example, typing "D2", then hitting enter twice and giving feedback will amount to a two-point deduction.

![Custom deduction](/tutorial/7.png)

If you create a comment like "D4: G7", then the grader will assess a four-point deduction, and also paste the contents of the deduction code `G7` in either `deductions_common.yaml` or `deductions_lab_specific.yaml` if it resides in the root of the repo. There are examples of these files in the `examples` folder of this repo. Be sure to copy them to the root of the repo, and modify as you see fit, in order to use this feature. This feature allows for common feedback to be duplicated exactly across reports. Below you can see that a comment that looks like the one labeled "Before" will produce the comment labeled "After" when re-running the grader.

![Deduction codes](/tutorial/6.png)

It is also possible to assess a deduction without taking off any points. Simply stating the deduction code will paste the contents of that deduction code without taking off points.

![Deduction code without points lost](/tutorial/11.png)

Finally, be careful about taking points off before the "ABSTRACT: 10/10" comment, because these points will not be tallied up. This may be fixed in the future, but for now, only make point-losing comments *after* the "ABSTRACT: 10/10" comment.

### Update the grade of the active report

When you're ready to update the grade of the report you're working on, run `update_grade.py`. You may also use the keyboard shortcut `Alt+W` if you have the AutoHotkey script running. This procedure can now be repeated for each report.

The total will be updated to reflect the total content points earned in this report, which sum up to 100 points. The deductions are subtracted from the content points, resulting in the grade received for this report. You may also summarize your feedback to the student in this comment block, as long as you don't disturb the first three lines of the comment it will still update when re-running `update_grade.py`.

![Example total](/tutorial/9.png)

A given section template comment might look like this. You can give a feedback summary to the student as long as you don't disturb the first line in the comment. This comment will still update when `update_grade.py` is re-run.

![Example section total](/tutorial/10.png)

### Update all grades again when finished

It is good practie to run `update_all_grades.py` once more after finishing grading. This will be sure that all reports have the latest grade tallied. When finished, you can close all lab reports with `close_all.py`.

## Workaround in case a certain script isn't working

If a script isn't working, especially `update_grade.py` via the AutoHotkey shortcut, is most likely caused by the "Call was rejected by callee" bug. When invoking the script from the keyboard shortcut, you will not be notified when the action fails, you will just see that the grade is not updated.

As far as I can tell, this is an unavoidable bug in the way that we're talking to Microsoft Word through the  [`pywin32`](https://github.com/mhammond/pywin32) library. A certain open document will be occasionally "infected" with this bug. If this happens when running the script from a PowerShell prompt, then you'll see the following traceback.

```PowerShell
Traceback (most recent call last):
  <lots of pointless text here>
pywintypes.com_error: (-2147418111, 'Call was rejected by callee.', None, None)
```

**The workaround:** You must save and close the affected document, then re-open it.
