# pylint: disable-all

import os
import sys

sys.path.insert(0, os.path.abspath(".."))
project = "grade_me380"
author = "Blake Naccarato"
copyright = f"2020, {author}"

extensions = ["sphinx.ext.napoleon", "sphinx.ext.autodoc"]

add_module_names = False
autodoc_member_order = "bysource"
autodoc_typehints = "description"

html_theme = "sphinx_rtd_theme"
