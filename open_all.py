"""Open all documents in preparation for grading."""

from __future__ import annotations

from typing import Optional

import docxrev
import fire
from win32com.client import constants

import shared
from shared import Path


def open_all(directory: Optional[Path] = None):
    """Open all documents in preparation for grading.

    Open documents in `directory` in preparation for grading. If `directory` is not
    supplied, then use the hardcoded `shared.directory` defined in `shared.py`.

    Args:
        directory: The directory containing the documents to open.
    """

    paths = shared.get_paths(directory)
    for path in paths:
        document = docxrev.Document(path, save_on_exit=False, close_on_exit=False)
        with document:
            document.com.ActiveWindow.View.SplitSpecial = constants.wdPaneRevisions


if __name__ == "__main__":
    fire.Fire(open_all)
