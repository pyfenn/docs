import os
import sys
# 1. Path Setup: Tell Sphinx to look at the repo root for the fenn code folder
sys.path.insert(0, os.path.abspath('..')) 

# -- Project information -----------------------------------------------------

project = "fenn"
copyright = "2026, pyfenn"  # Adjust year/author as preferred by the maintainer
author = "pyfenn"
master_doc = "index"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",      # Core extension to extract code docstrings
    "sphinx.ext.napoleon",     # Essential for parsing Fenn's Google-style docstrings
    "sphinx.ext.viewcode",     # Adds "[source]" links to view Python files directly
    "sphinx_copybutton",       
    "sphinx_design",           
]

# Type hints configuration (borrowed from Dishka for cleaner code reading)
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
    # Light mode theme adjustments
    "light_css_variables": {
        # A slightly deeper teal-green for legible contrast on a white background
        "color-brand-primary": "#00A86B",  
        "color-brand-content": "#00A86B",  
    },
    # Dark mode theme adjustments
    "dark_css_variables": {
        # That brilliant electric mint green straight from your Fenn banner!
        "color-brand-primary": "#00C887",  
        "color-brand-content": "#00C887",  
    },
}