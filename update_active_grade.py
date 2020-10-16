"""Update the grade of the active document."""

from __future__ import annotations

import pathlib
from typing import Optional
from warnings import warn

import docxrev
import fire

import shared
from shared import Path
from update_grade import update_grade


def update_active_grade(
    directory: Optional[Path] = None, gradebook_path: Optional[Path] = None
):
    """Update the grade of the active document.

    Update the grade from the active document, and the gradebook. Ensure that the active
    document and gradebook is as as specified in :py:func:`shared.get_paths`.

    Parameters
    ----------
    directory
        The directory where the active document should reside.
    gradebook_name
        The name of the gradebook (include ".csv"). Defaults to "grades.csv". Warn if
        different than expected.
    """

    (paths, automatic_gradebook_path) = shared.get_paths(directory)

    if gradebook_path is None:
        gradebook_path = automatic_gradebook_path
    else:
        gradebook_path = pathlib.Path(gradebook_path)

    if gradebook_path is not None and gradebook_path != automatic_gradebook_path:
        warn("Supplied gradebook different than expected one.")

    # First check if the document is in paths without saving
    active_document = docxrev.get_active_document(save_on_exit=False)
    with active_document:
        is_in_paths = active_document.path in paths  # we consume `paths` here

    # Now update the grade or raise an exception
    if is_in_paths:
        active_document.save_on_exit = True
        update_grade(active_document, gradebook_path)
    else:
        raise Exception("Active document not in paths.")


if __name__ == "__main__":
    fire.Fire(update_active_grade)  # CLI
    docxrev.quit_word_safely()  # If used as a CLI, quit Word if nothing was open
