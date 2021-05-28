# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
# sys.path.insert(0, os.path.abspath('.'))
sys.path.append( os.path.dirname( os.getcwd() ) )


# -- Project information -----------------------------------------------------

project = 'CerebUnit'
copyright = '2021, Lungsi'
author = 'Lungsi'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "recommonmark",
    "nbsphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx.ext.mathjax",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# to avoid breaking the building process due to external dependencies not met
autodoc_mock_imports = [
    "neuron", "sciunit", "executive", "ExecutiveControl",
    "scipy", "numpy", "quantities", "cerebstats"
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'bizstyle'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#html_static_path = ['_static']
#html_static_path = ["_static", "statistics/guides"]
#html_extra_path = [os.getcwd()+os.sep+"statistics"+os.sep+"guides"]
#html_extra_path = [os.getcwd()+"/statistics/guides/statistics_definitions.html",
#                   "statistics/guides/images/.png",
#                   "statistics/guides/scripts/.js"]
#html_css_files = ["statistics/guides/scripts/style.css"]
#html_js_files = ["statistics/guides/scripts/mootools-core-1.3.1.js",
#                 "statistics/guides/scripts/Tangle.js",
#                 "statistics/guides/scripts/main.js"]
#html_extra_path = ["statistics/guides/statistics_definitions.html"]

# -- Options for Notebooks ---------------------------------------------------

# Execute in advance. If notebooks tests code you may run them at build time.
nbsphinx_execute = "never"
nbsphinx_allow_errors = True

#source_suffix = [".rst", ".ipynb"]
