# Configuration file for the Sphinx documentation builder.
#
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "kernel-sign"
copyright = '2023-present, Gene C'
author = 'Gene C'
release = "5.0.1"

#extensions = ['myst_parser']
extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'Misc/*', 'Changelog.rst']


html_theme = 'alabaster'
html_static_path = ['_static']
