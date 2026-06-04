import os
import sys


_parent = os.path.abspath('..')
if os.path.exists(os.path.join(_parent, 'fenn', '__init__.py')):
    sys.path.insert(0, _parent)

# -- Project information -----------------------------------------------------
project = "fenn"
copyright = "2026, pyfenn"
author = "pyfenn"
master_doc = "index"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
    "myst_parser",        # Allows Sphinx to read existing MkDocs .md files
]

# MyST Parser settings — enable all common extensions
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "tasklist",
]

# Tell Sphinx to look in src/ for the existing MkDocs markdown content
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

autodoc_typehints = "description"
autodoc_type_aliases = {}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
html_theme = "furo"
html_title = "Fenn Documentation"
html_logo = "_static/logo.png"
html_favicon = "_static/favicon.ico"
html_theme_options = {
    "source_repository": "https://github.com/pyfenn/fenn",
    "source_branch": "main",
    "source_directory": "docs/",
    "light_css_variables": {
        "color-brand-primary": "#00A86B",
        "color-brand-content": "#00A86B",
    },
    "dark_css_variables": {
        "color-brand-primary": "#00C887",
        "color-brand-content": "#00C887",
    },
}