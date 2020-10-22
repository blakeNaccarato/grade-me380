# pylint: disable-all

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(r"..\src\docxrev").resolve()))
project = "grade_me380"
author = "Blake Naccarato"
copyright = f"2020, {author}"

extensions = ["sphinx.ext.napoleon", "sphinx.ext.autodoc"]

templates_path = ['_templates']
exclude_patterns = ['..\\docs', 'Thumbs.db', '.DS_Store']

add_module_names = False
autodoc_member_order = "bysource"
autodoc_typehints = "description"

html_theme = "sphinx_rtd_theme"
