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

```ps1
# If there is a Python virtual environment in the PWD, activate it
$PATH_VENV = ".\.venv\Scripts\Activate.ps1"
if (Test-Path $PATH_VENV) { & $PATH_VENV }
```

You can navigate to your PowerShell profile by typing the following in the PowerShell prompt:

```ps1
notepad $PROFILE
```

Copying the snippet into your PowerShell profile and saving the file will ensure that a virtual environment in your current directory is activated whenever PowerShell is launched. This is needed for the AutoHotkey scripts to work properly.

### Create a virtual environment and activate it

Make sure that your PowerShell prompt is currently in the repo folder that you cloned (e.g. `C:/Users/You/grade-me380`). Then, enter the following:

```ps1
py -m venv .venv
```

Heads up, a quick way to open PowerShell in a folder is through the right-click context menu. You may need to reboot after installing PowerShell 7 for the first time if you don't see this.

![Open PowerShell here](/tutorial/4.png)

Open a PowerShell prompt in the root of the cloned repo and it should look like the following, with `(.venv)` at the start of the prompt. If it doesn't, then you didn't modify your PowerShell `$PROFILE` properly. Go back to that step and make sure the profile is properly set up.

![Activated virtual environment](/tutorial/5.png)

### Download submissions

Download the submissions you want to grade.

![Download submissions](/tutorial/1.png)

### Extract submissions

Extract the submissions to a folder. Keep the default folder name `submissions`.

![Extract submissions](/tutorial/2.png)

### Move submissions folder into the root of the cloned repo

![Move submissions ](/tutorial/3.png)

### Launch the autohotkey scripts

Double-click the scripts `hotkey_toggle_review_pane.ahk` and `hotkey_update_active_grade.ahk`. Note that these will bind the keyboard shortcut `Alt+W` to run the `update_active_grade.py` script, and  `Ctrl+Alt+W` to the `toggle_active_review_pane.py` script.
