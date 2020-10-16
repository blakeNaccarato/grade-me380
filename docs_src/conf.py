# pylint: disable-all

import os
import sys

sys.path.insert(0, os.path.abspath(".."))
author = "Blake Naccarato"
copyright = f"2020, {author}"

extensions = ["sphinx.ext.napoleon", "sphinx.ext.autodoc"]

autodoc_member_order = "bysource"

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
