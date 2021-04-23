"""Shared values."""

from __future__ import annotations

import os
from pathlib import Path
import re
from typing import Iterator, Optional, Tuple

__all__ = ["get_paths"]


# * -------------------------------------------------------------------------------- * #
# * PATHS

ENV_KEYS = ["GRADEBOOK_NAME", "DOCX_DIRECTORY"]
ENV = {key: os.getenv(key) for key in ENV_KEYS}

if ENV["GRADEBOOK_NAME"] is None:
    GRADEBOOK_NAME = "grades.csv"
else:
    GRADEBOOK_NAME = ENV["GRADEBOOK_NAME"]

if ENV["DOCX_DIRECTORY"] is None:
    DOCX_DIRECTORY = Path().cwd()
else:
    DOCX_DIRECTORY = Path(ENV["DOCX_DIRECTORY"])

DOCX = r"[!~$]*.docx"  # excludes "~$" prefix temporary files
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
    r"(?P<content>TOTAL CONTENT: )-?\d+\r"
    r"(?P<deductions>TOTAL DEDUCTIONS: )-?\d+\r"
    r"(?P<grade>GRADE: )-?\d+"
)

# The header comments to be inserted
HEADER_COMMENTS = [
    f"{header.upper()}: {score}/{score}"
    for header, score in zip(FULL_HEADERS, MAX_SCORES)
]
# The pattern for finding header comments as well as substituting scores within them
HEADER_COMMENT_PATTERNS = [
    re.compile(fr"(?P<header>{header.upper()}: )-?\d+") for header in FULL_HEADERS
]


# * -------------------------------------------------------------------------------- * #
# * SCORING
# Patterns here use named groups to be reused during scoring operations.

# Matches comments with a number at the very start of the comment
CONTENT_POINTS_LOST_PATTERN = re.compile(r"(?P<value>-?\d+)")

# Matches comments with "D", then a number, at the very start of the comment
DEDUCTION_PATTERN = re.compile(r"D(?P<value>-?\d+)")


# * -------------------------------------------------------------------------------- * #
# * FUNCTIONS


def get_paths(
    directory: Optional[Path] = None,
    gradebook_name: Optional[str] = GRADEBOOK_NAME,
) -> Tuple[Iterator[Path], Path]:
    """Get paths to all documents in a directory and the gradebook.

    Get paths to all documents in whichever comes first of the following: `directory`,
    the environment variable `DOCX_DIRECTORY`, or the current working directory. Also
    get the path to the gradebook (default "grades.csv"), which is put in the same
    directory as the documents.

    Parameters
    ----------
    directory
        The directory to get documents from.
    gradebook_name
        The name of the gradebook. Defaults to "grades.csv".

    Returns
    -------
    paths
        Paths to documents.
    gradebook_path
        Path to the gradebook.
    """

    if directory is None:
        paths = PATHS
    else:
        docx_directory = Path(directory)
        paths = docx_directory.glob(DOCX)

    if gradebook_name is None:
        gradebook_name = GRADEBOOK_NAME
    else:
        gradebook_path = DOCX_DIRECTORY / GRADEBOOK_NAME

    return paths, gradebook_path
