"""Toggle the review pane of the active document."""

from __future__ import annotations

from typing import Optional

import docxrev
import fire
from win32com.client import constants

import shared
from shared import Path


def toggle_active_review_pane(directory: Optional[Path] = None):
    """Toggle the review pane of the active document.

    Update the grade from the active document, and the gradebook. Ensure that the active
    Ensure that the active document and gradebook is as as specified in
    :py:func:`shared.get_paths`.

    Parameters
    ----------
    directory
        The directory where the active document should reside.
    """

    (paths, _) = shared.get_paths(directory)

    active_document = docxrev.get_active_document(save_on_exit=False)
    with active_document:
        # Check if the document is in paths
        in_paths = active_document.path in paths  # we consume `paths` here
        # Now update the grade or raise an exception
        if in_paths:
            active_document.com.ActiveWindow.View.SplitSpecial = (
                constants.wdPaneRevisions
            )
        else:
            raise Exception("Active document not in paths.")


if __name__ == "__main__":
    fire.Fire(toggle_active_review_pane)  # CLI
    docxrev.quit_word_safely()  # If used as a CLI, quit Word if nothing was open
