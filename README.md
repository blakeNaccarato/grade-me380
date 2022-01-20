# Grade ME380

The scripts in this repo can be used to automate scoring of assignments. These scripts do not perform any "intelligent" actions such as detecting content or formatting issues, they simply keep track of points lost and allow for the grader to quickly insert "canned responses" for very common issues (e.g. "Wrong title page").

## Installation

- Clone this repo.
- Create a virtual environment in the root of the cloned repo and activate it in your IDE.
- Install the requirements in `requirements.txt`.
- Copy the YAML files from `examples` to the root of the repo, or supply your own (names must match exactly).
- Copy the `.env` file from `examples` to the root of the repo, or supply your own.
- Install AutoHotkey if you haven't already.

Now you should be able to launch the AutoHotkey scripts, which will attach the two most important scripts, `update_active_grade.py` and `toggle_review_pane.py` to keyboard shortcuts `Alt+W` and `Ctrl+Alt+W` respectively.

You can also run scripts directly in your IDE or from the command line. Other useful scripts are `open_all.py`, `save_all.py`, and `close_all.py`.
