"""Delete all comments from all documents."""

from __future__ import annotations

from typing import Optional

import docxrev
import fire

import shared
from shared import Path


def delete_all_comments(directory: Optional[Path] = None):
    """Delete all comments from all documents.

    Delete all comments from all documents in `directory` as specified in
    :py:func:`shared.get_paths`.

    Parameters
    ----------
    directory
        The directory containing the documents.
    """

    response = input(  # nosec
        "Are you sure you want to delete all comments? [y/N] >>> "
    )
    if response.lower() == "y":
        (paths, _) = shared.get_paths(directory)
        for path in paths:
            docxrev.Document(path).delete_comments()
    else:
        print("Not deleting comments.")


if __name__ == "__main__":
    fire.Fire(delete_all_comments)  # CLI
    docxrev.quit_word_safely()  # If used as a CLI, quit Word if nothing was open
