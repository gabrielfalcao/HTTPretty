# -*- coding: utf-8 -*-

import sys
import sphinx_rtd_theme
try:
    from pathlib2 import Path
except ImportError:
    from pathlib import Path

project_path = Path(__file__).absolute().parent.joinpath('../..')

sys.path.insert(0, project_path.as_posix())

from httpretty.version import version # noqa


project = 'HTTPretty'
copyright = '2011-2021, Gabriel Falcao'
author = 'Gabriel Falcao'

# The short X.Y version
version = version
# The full version, including alpha/beta/rc tags
release = version


extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.autosummary',
    'sphinx.ext.autosummary',
    'sphinxcontrib.asciinema',
]

templates_path = ['_templates']

source_suffix = '.rst'
master_doc = 'index'
language = None
exclude_patterns = []
pygments_style = 'friendly'
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
# html_theme_options = {}
html_static_path = ['_static']

htmlhelp_basename = 'HTTPrettydoc'

latex_elements = {}

latex_documents = [
    (master_doc, 'HTTPretty.tex', 'HTTPretty Documentation',
     'Gabriel Falcao', 'manual'),
]

man_pages = [
    (master_doc, 'httpretty', 'HTTPretty Documentation',
     [author], 1)
]


texinfo_documents = [
    (master_doc, 'HTTPretty', 'HTTPretty Documentation',
     author, 'HTTPretty', 'One line description of project.',
     'Miscellaneous'),
]


epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

epub_exclude_files = ['search.html']
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),

    'httplib2': ('https://httplib2.readthedocs.io/en/latest/', None),
    'requests': ('https://requests.readthedocs.io/en/master/', None),
    'urllib3': ('https://urllib3.readthedocs.io/en/latest/', None),
}
