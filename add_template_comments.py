"""Add template comments to all documents in the directory."""

from __future__ import annotations

from typing import Optional

import docxrev
import fire
from win32com.client import constants

import shared
from shared import Path


def add_template_comments(directory: Optional[Path] = None):
    """Add template comments to all documents in the directory.

    Add template comments to all documents in `directory`. If `directory` is not
    supplied, then use the hardcoded paths defined in `shared.PY`.

    Args:
        directory: The directory containing the documents to add template comments to.
    """

    paths = shared.get_paths(directory)

    for path in paths:
        with docxrev.Document(path) as document:

            # Convenient access to COM objects
            com_selection = document.com.Windows(1).Selection
            com_find = com_selection.Find

            document.com.Application.CommandBars.ExecuteMso("TableOfContentsRemove")

            # Go to the top of the document and add the summary comment
            com_selection.HomeKey(constants.wdStory)
            com_selection.Comments.Add(
                Range=com_selection.Range, Text=shared.SUMMARY_COMMENT
            )

            # Find headers and add header comments pointing to them
            for header, header_comment in zip(shared.HEADERS, shared.HEADER_COMMENTS):

                # Find the header
                com_find.Execute(
                    FindText=header,  # Find the header
                    # Ensure certain `Find` options are set
                    Forward=True,
                    MatchCase=False,
                    MatchWholeWord=False,
                    MatchWildcards=False,
                    MatchSoundsLike=False,
                    MatchAllWordForms=False,
                    Wrap=False,
                    Format=False,
                    Replace=constants.wdReplaceNone,
                )

                # Add the header comment pointing to the `Range` just found
                com_selection.Comments.Add(
                    Range=com_selection.Range,
                    Text=header_comment,
                )
                com_selection.EndKey()

            # Go back to the top of the document when done
            com_selection.HomeKey(constants.wdStory)


if __name__ == "__main__":
    fire.Fire(add_template_comments)  # CLI
    docxrev.quit_word_safely()  # If used as a CLI, quit Word if nothing was open
