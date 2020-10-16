"""Shared values."""

from __future__ import annotations

import pathlib
import re
from typing import Iterator, Optional, Union
import os

Path = Union[str, os.PathLike]

# * -------------------------------------------------------------------------------- * #
# * PATHS


# Paths
GRADEBOOK_NAME = "grades.csv"
DOCX = r"[!~$]*.docx"  # excludes "~$" prefix temporary files
# docx_directory = pathlib.Path(r".\submissions\1003")
DOCX_DIRECTORY = pathlib.Path(r".\submissions\test")
PATHS = DOCX_DIRECTORY.glob(DOCX)
GRADEBOOK_PATH = DOCX_DIRECTORY / GRADEBOOK_NAME

# * -------------------------------------------------------------------------------- * #
# * COMMENTS
# Patterns here use named groups to be reused during replacement operations.

# For searching document content to insert comments
HEADERS = [
    "abstract",
    "introduction",
    "procedures",
    "results and discussion",
    "conclusion",
]

# For the actual content of the inserted comments
FULL_HEADERS = [
    "abstract",
    "introduction and theory",  # different
    "procedures",
    "results and discussion",
    "conclusion",
]
MAX_SCORES = [10, 20, 20, 40, 10]

# The summary to be inserted and its pattern for later updating by regex
SUMMARY_COMMENT = "TOTAL CONTENT: 100\nTOTAL DEDUCTIONS: 0\nGRADE: 100/100"
# We match on "\r" because Microsoft Word implicitly converts "\n" to "\r" on insertion
SUMMARY_COMMENT_PATTERN = re.compile(
    r"(?P<content>TOTAL CONTENT: )\d+\r"
    r"(?P<deductions>TOTAL DEDUCTIONS: )\d+\r"
    r"(?P<grade>GRADE: )\d+"
)

# The header comments to be inserted
HEADER_COMMENTS = [
    f"{header.upper()}: {score}\\{score}"
    for header, score in zip(FULL_HEADERS, MAX_SCORES)
]
# The pattern for finding header comments as well as substituting scores within them
HEADER_COMMENT_PATTERNS = [
    re.compile(fr"(?P<header>{header.upper()}: )\d+") for header in FULL_HEADERS
]

# * -------------------------------------------------------------------------------- * #
# * SCORING
# Patterns here use named groups to be reused during scoring operations.

# Matches comments with a number at the very start of the comment
CONTENT_POINTS_LOST_PATTERN = re.compile(r"(?P<value>\d+)")

# Matches comments with "D", then a number, at the very start of the comment
DEDUCTION_PATTERN = re.compile(r"D(?P<value>\d+)")


# * -------------------------------------------------------------------------------- * #
# * FUNCTIONS


def get_paths(directory: Optional[Path] = None) -> Iterator[os.PathLike]:
    """Get the paths to all documents in a directory.

    Get the paths to all documents in a directory or else just return the paths
    specified in `shared.py`.

    Args:
        directory: The directory to get documents from.
    """

    if directory is None:
        paths = PATHS
    else:
        paths = pathlib.Path(directory).glob(DOCX)

    return paths
