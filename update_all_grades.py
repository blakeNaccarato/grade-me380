"""Update all grades."""

from __future__ import annotations

import pathlib
from typing import Optional

import docxrev
import fire

import shared
from shared import Path
from update_grade import update_grade


def update_all_grades(
    directory: Optional[Path] = None, gradebook_path: Optional[Path] = None
):
    """Update all grades.

    Args:
        directory: The directory to update grades in.
        gradebook_path: The gradebook to update.
    """

    paths = shared.get_paths(directory)
    if gradebook_path is None:
        gradebook_path = shared.GRADEBOOK_PATH
    else:
        gradebook_path = pathlib.Path(gradebook_path)

    for path in paths:
        document = docxrev.Document(path)
        update_grade(document, gradebook_path)


if __name__ == "__main__":
    fire.Fire(update_all_grades)  # CLI
    docxrev.quit_word_safely()  # If used as a CLI, quit Word if nothing was open
