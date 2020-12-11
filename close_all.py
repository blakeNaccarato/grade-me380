"""Save and close all documents."""

from __future__ import annotations

from typing import Optional

import docxrev
import fire

import shared
from shared import Path


def close_all(directory: Optional[Path] = None):
    """Save and close all documents.

    Save and close all documents in `directory` as specified in
    :py:func:`shared.get_paths`.

    Parameters
    ----------
    directory
        The directory containing the documents.
    """

    (paths, _) = shared.get_paths(directory)
    for path in paths:
        document = docxrev.Document(path, save_on_exit=True, close_on_exit=True)
        with document:
            pass


if __name__ == "__main__":
    fire.Fire(close_all)
