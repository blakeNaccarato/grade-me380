"""Delete all comments from all documents in the directory."""

from __future__ import annotations

from typing import Optional

import docxrev
import fire

import shared
from shared import Path


def delete_all_comments(directory: Optional[Path] = None):
    """Delete all comments from all documents in the directory.

    Delete all comments from all documents in `directory`. If `directory` is not
    supplied, then use the hardcoded paths defined in `shared.py`.

    Args:
        directory: The directory containing the documents with comments to be deleted.
    """

    paths = shared.get_paths(directory)
    for path in paths:
        docxrev.Document(path).delete_comments()


if __name__ == "__main__":
    fire.Fire(delete_all_comments)  # CLI
    docxrev.quit_word_safely()  # If used as a CLI, quit Word if nothing was open
