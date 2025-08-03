# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'thinking-in-langchain'
copyright = '2025, pfnie'
author = 'pfnie'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
     'recommonmark',
     'sphinx_markdown_tables'
 ]

templates_path = ['_templates']
exclude_patterns = []


# add "Edit on Github"
html_context = {
	"display_github": True,
	"github_user":"pengfeinie",
	"github_repo":"thinking-in-langchain",
	"github_version":"main/source/"
}



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = [
    'custom.css',
]

# If true, links to the reST sources are added to the pages.
#
html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#
html_show_sphinx = True

html_theme_options = {
    'navigation_depth': 2, #根据实际需求调整
    'collapse_navigation': False,
    'sticky_navigation': True,
}
