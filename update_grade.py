"""Update a document's grade as well as the gradebook."""
from __future__ import annotations

import csv
import os
from dataclasses import dataclass
from typing import Any, Iterator, List

import docxrev

import shared

from dynaconf import Dynaconf

common_deductions = Dynaconf(settings_files=["deductions.yaml"]).deductions

__all__ = ["update_grade"]


def update_grade(document: docxrev.Document, gradebook_path: os.PathLike):
    """Update a document's grade as well as the gradebook.

    Parameters
    ----------
    document
        Document.
    gradebook_path
        Gradebook.
    """

    with document:
        grade = grade_document(document)
        update_document_scores(document, grade)
        update_gradebook(document, gradebook_path, grade)


def grade_document(document: docxrev.Document) -> Grade:
    """Grade a document.

    Parameters
    ----------
    document
        Document.
    """

    # Search comments in reverse. This means that point deductions in any given section
    # will be encountered before we reach the header comment. This allows us to walk
    # through the comments once, and exit cleanly once we reach the first header
    # comment. We use `iter` and `next` on `comments` because they advance at a
    # different pace than the `header_comment_patterns` and `max_scores`.
    comments = iter(reversed(document.comments))
    header_comment_patterns = reversed(shared.HEADER_COMMENT_PATTERNS)
    max_scores = reversed(shared.MAX_SCORES)

    # Prepare the lists to be returned. They will be reversed at the end.
    scores: List[int] = []
    header_comments: List[docxrev.com.Comment] = []
    deductions = 0

    # Get the scores for each section
    comment = safe_next(comments)
    for header_comment_pattern, max_score in zip(header_comment_patterns, max_scores):

        # Process point deductions while we don't recognize a header comment
        content_points_lost = 0
        while not header_comment_pattern.match(comment.text):

            # Increment the points lost in this section for matching comments
            match = shared.CONTENT_POINTS_LOST_PATTERN.match(comment.text)
            if match:
                content_points_lost += int(match["value"])

            # Increment total deductions for matching comments
            match = shared.DEDUCTION_PATTERN.match(comment.text)
            if match:
                deductions += int(match["value"])

            # Add text description to common deduction codes found in the document
            matches = [
                pattern.match(comment.text)
                for pattern in shared.COMMON_DEDUCTION_PATTERNS
            ]
            match = matches[0] or matches[1] or matches[2]
            if any(matches):
                first_match = [match for match in matches if match][0]
                first_line_of_comment = comment.text.split("\r", maxsplit=1)[0]
                deduction_text = [
                    deduction.text
                    for deduction in common_deductions
                    if first_match["code"] == deduction.code
                ][0]
                comment.update(first_line_of_comment + "\n\n" + deduction_text)

            # Try to get the next comment, raising an error if there are none left
            comment = safe_next(comments)

        # We found a header comment. Store it and move on.
        header_comments.append(comment)
        comment = safe_next(comments)

        # Store the score for this section and skip the header comment
        scores.append(max_score - content_points_lost)

    header_comments.reverse()
    scores.reverse()
    grade = Grade(header_comments, scores, deductions)

    return grade


def update_document_scores(document: docxrev.Document, grade: Grade):
    """Update document scores with the determined grade.

    Parameters
    ----------
    document
        Document.
    grade
        Grade.
    """

    # Update the summary comment scores
    summary_comment = document.comments[0]
    substitution = (
        fr"\g<content>{grade.content}\n"
        fr"\g<deductions>{grade.deductions}\n"
        fr"\g<grade>{grade.total}"
    )
    summary_comment.update(
        shared.SUMMARY_COMMENT_PATTERN.sub(substitution, summary_comment.text)
    )

    # Update the scores of the header comments
    for comment, pattern, score in zip(
        grade.header_comments, shared.HEADER_COMMENT_PATTERNS, grade.scores
    ):
        substitution = fr"\g<header>{score}"
        comment.update(pattern.sub(substitution, comment.text))


def update_gradebook(
    document: docxrev.Document, gradebook_path: os.PathLike, grade: Grade
):
    """Write the grade for the paper being graded to a CSV file.

    Parameters
    ----------
    gradebook_path
        Gradebook.
    document
        Document.
    grade
        Grade.
    """

    # Prepare rows for the CSV
    header_row = ["Document", "Grade", "Total Content", "Total Deductions"]
    header_row.extend([header.upper() for header in shared.FULL_HEADERS])
    new_row = [document.name, grade.total, grade.content, grade.deductions]
    new_row.extend(grade.scores)
    rows_to_write: List[Any] = []

    # Create the CSV and write the header if it doesn't exist
    if not os.path.exists(gradebook_path):
        with open(gradebook_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header_row)

    # Build the rows of the CSV, overwriting or appending the current paper being graded
    with open(gradebook_path, "r", newline="") as file:

        update_existing_row = False
        reader = csv.reader(file)
        next(reader)  # skip the header

        # If the paper has already been graded, update that row, otherwise append it
        for row in reader:
            if row and new_row[0] == row[0]:
                rows_to_write.append(new_row)
                update_existing_row = True
            else:
                rows_to_write.append(row)
        if not update_existing_row:
            rows_to_write.append(new_row)

    # Write the updated file
    with open(gradebook_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header_row)
        for row in rows_to_write:
            writer.writerow(row)


def safe_next(comments: Iterator[docxrev.com.Comment]) -> docxrev.com.Comment:
    """Safely get the next comment.

    Safely get the next comment, raising an error if all comments have been exhausted.

    Parameters
    ----------
    comments
        A comment iterator.
    document
        The document.

    Raises
    ------
    StopIteration
        If all comments are exhausted.
    """
    try:
        comment = next(comments)
    except StopIteration as error:
        message = (
            f"Exhausted comments in {comment.in_document.name}"
            f"before finding all header comments."
        )
        raise type(error)(message) from error

    return comment


@dataclass
class Grade:
    """A grade."""

    header_comments: List[docxrev.com.Comment]
    """Header comments."""

    scores: List[int]
    """Scores."""

    deductions: int
    """Deductions."""

    @property
    def content(self) -> int:
        """Content score."""
        return sum(self.scores)

    @property
    def total(self) -> int:
        """Total score."""
        return self.content - self.deductions
