# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sphinxawesome_theme']

package_data = \
{'': ['*'], 'sphinxawesome_theme': ['static/*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'docutils<0.17',
 'sphinx>3',
 'sphinxawesome-sampdirective>=1.0.3,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.1,<3.0.0']}

entry_points = \
{'sphinx.html_themes': ['sphinxawesome_theme = sphinxawesome_theme']}

setup_kwargs = {
    'name': 'sphinxawesome-theme',
    'version': '1.19.3',
    'description': 'An awesome theme for the Sphinx documentation generator',
    'long_description': 'Sphinx awesome theme\n====================\n\n.. image:: https://img.shields.io/pypi/l/sphinxawesome-theme?color=blue\n   :target: https://opensource.org/licenses/MIT\n   :alt: MIT license\n\n.. image:: https://img.shields.io/pypi/v/sphinxawesome-theme\n   :target: https://pypi.org/project/sphinxawesome-theme\n   :alt: PyPI package version number\n\n.. image:: https://api.netlify.com/api/v1/badges/e6d20a5c-b49e-4ebc-80f6-59fde8f24e22/deploy-status\n   :target: https://app.netlify.com/sites/sphinxawesome-theme/deploys\n   :alt: Netlify Status\n\n.. readme-start\n\nThis is an awesome theme and a set of extensions\nfor the Sphinx_ documentation generator.\nUsing this theme and extension,\nyou can change the look of your documentation website\nand add a number of useful improvements.\nSee the theme in action at https://sphinxawesome.xyz.\n\n.. _Sphinx: http://www.sphinx-doc.org/en/master/\n\nGetting started\n---------------\n\nYou can install the awesome theme from the Python package index\nand modify the Sphinx configuration file ``conf.py``.\n\nTo get started using this theme, follow these steps:\n\n#. Install the theme as a Python package.\n\n   .. code:: console\n\n      $ pip install sphinxawesome-theme\n\n\n   See `How to install the theme`_ for more information.\n\n   .. _How to install the theme: https://sphinxawesome.xyz/how-to/install\n\n#. Add the ``html_theme`` configuration option\n   to the Sphinx configuration file ``conf.py``.\n\n   .. code:: python\n\n      html_theme = "sphinxawesome_theme"\n\n   See `How to use the theme`_ for more information.\n\n   .. _How to use the theme: https://sphinxawesome.xyz/how-to/use\n\nFeatures\n--------\n\nThis theme is designed with readability and usability in mind.\nThe theme includes several extensions that enhance the usability:\n\nAwesome code blocks\n    - Code blocks have a header section, displaying the optional caption,\n      as well as the programming language used for syntax highlighting\n    - The code block headers contain a **Copy** button, allowing you to copy\n      code snippets to the clipboard.\n    - The theme adds two new options to Sphinx\'s ``code-block`` directive:\n      ``emphasize-added`` and ``emphasize-removed``, allowing you to highlight\n      code changes within other highlighted code.\n\nAwesome new directive for highlighting placeholder variables\n    The theme supports a new directive ``samp``, which is the equivalent of the\n    built-in ``:samp:`` interpreted text role. This allows you to highlight placeholder\n    variables in code blocks.\n\nAwesome user experience improvements\n    These small features make the theme more usable. To name a few:\n    \n    - better keyboard navigation:\n    \n      - use the ``Tab`` key to navigate through all sections on the page\n      - use the *Skip to Content* link to bypass the navigation links\n      - use the ``/`` key (forward Slash) to focus the search input element\n      \n    - better “permalink” mechanism:\n    \n      - hovering over an element with a permalink reveals a *Link* icon\n      - selecting the *Link* icon copies the link to the clipboard\n      - notes, warnings and other admonitions have permalinks by default\n      \n    - collapsible elements: \n    \n      - nested navigation links – all pages are reachable from all other pages\n      - code definitions – code object definitions (functions, classes, modules, etc.), for example obtained via the ``sphinx.ext.autodoc`` extension.\n',
    'author': 'Kai Welke',
    'author_email': 'kai687@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kai687/sphinxawesome-theme',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
