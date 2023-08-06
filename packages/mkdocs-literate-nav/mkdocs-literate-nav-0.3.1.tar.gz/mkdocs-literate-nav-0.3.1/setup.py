# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs_literate_nav']

package_data = \
{'': ['*']}

install_requires = \
['glob2>=0.7,<0.8', 'mkdocs>=1.0,<2.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

entry_points = \
{'mkdocs.plugins': ['literate-nav = '
                    'mkdocs_literate_nav.plugin:LiterateNavPlugin']}

setup_kwargs = {
    'name': 'mkdocs-literate-nav',
    'version': '0.3.1',
    'description': 'MkDocs plugin to specify the navigation in Markdown instead of YAML',
    'long_description': '# mkdocs-literate-nav\n\n**[Plugin][] for [MkDocs][] to specify the navigation in Markdown instead of YAML**\n\n[![PyPI](https://img.shields.io/pypi/v/mkdocs-literate-nav)](https://pypi.org/project/mkdocs-literate-nav/)\n[![GitHub](https://img.shields.io/github/license/oprypin/mkdocs-literate-nav)](https://github.com/oprypin/mkdocs-literate-nav/blob/master/LICENSE.md)\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/oprypin/mkdocs-literate-nav/CI)](https://github.com/oprypin/mkdocs-literate-nav/actions?query=event%3Apush+branch%3Amaster)\n\n```shell\npip install mkdocs-literate-nav\n```\n\nWorks well with **[section-index][]**. Supplants **[awesome-pages][]**.\n\n[mkdocs]: https://www.mkdocs.org/\n[plugin]: https://www.mkdocs.org/user-guide/plugins/\n[section-index]: https://oprypin.github.io/mkdocs-section-index/\n[awesome-pages]: https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin\n\n## Usage\n\nActivate the plugin in **mkdocs.yml**:\n\n```yaml\nplugins:\n  - search\n  - literate-nav:\n      nav_file: SUMMARY.md\n```\n\nand **drop** the `nav` section if it\'s present there; it will be ignored now.\n\n<table markdown="1"><tr>\n<td>To get this navigation,</td>\n<td>create the file <b>SUMMARY.md</b>:</td>\n<td>(old YAML equivalent:)</td>\n</tr><tr><td>\n\n* [Frob](#index.md)\n* [Baz](#baz.md)\n* [Borgs](#borgs/index.md)\n    * [Bar](#borgs/bar.md)\n    * [Foo](#borgs/foo.md)\n\n</td><td>\n\n```markdown\n* [Frob](index.md)\n* [Baz](baz.md)\n* [Borgs](borgs/index.md)\n    * [Bar](borgs/bar.md)\n    * [Foo](borgs/foo.md)\n```\n\n</td><td>\n\n```yaml\nnav:\n  - Frob: index.md\n  - Baz: baz.md\n  - Borgs:\n    - borgs/index.md\n    - Bar: borgs/bar.md\n    - Foo: borgs/foo.md\n```\n\n</td></tr></table>\n\nNote that, the way we wrote the Markdown, a section seems to also have a page associated with it. MkDocs doesn\'t actually support that, and neither is it representable in YAML directly, so the plugin tries to do the next best thing: include the link as the first page of the section. However, this structure is perfectly suited for the **[section-index][]** plugin, which actually makes this work. Or you could just *not* associate a link with sections:\n\n<table markdown="1"><tr>\n<td>To get this navigation,</td>\n<td>create the file <b>SUMMARY.md</b>:</td>\n<td>(old YAML equivalent:)</td>\n</tr><tr><td>\n\n* [Frob](#index.md)\n* [Baz](#baz.md)\n* Borgs\n    * [Bar](#borgs/bar.md)\n    * [Foo](#borgs/foo.md)\n\n</td><td>\n\n```markdown\n* [Frob](index.md)\n* [Baz](baz.md)\n* Borgs\n    * [Bar](borgs/bar.md)\n    * [Foo](borgs/foo.md)\n```\n\n</td><td>\n\n```yaml\nnav:\n  - Frob: index.md\n  - Baz: baz.md\n  - Borgs:\n    - Bar: borgs/bar.md\n    - Foo: borgs/foo.md\n```\n\n</td></tr></table>\n\n#### Nav cross-link\n\nBut why stop there? Each directory can have its own decoupled navigation list (see how the trailing slash initiates a nav cross-link):\n\n<table markdown="1"><tr>\n<td>To get this navigation,</td>\n<td>create the file <b>SUMMARY.md</b>:</td>\n<td>(old YAML equivalent:)</td>\n</tr><tr><td rowspan="3">\n\n* [Frob](#index.md)\n* [Baz](#baz.md)\n* Borgs\n    * [Bar](#borgs/bar.md)\n    * [Foo](#borgs/foo.md)\n\n</td><td>\n\n```markdown\n* [Frob](index.md)\n* [Baz](baz.md)\n* [Borgs](borgs/)\n```\n\n</td><td rowspan="3">\n\n```yaml\nnav:\n  - Frob: index.md\n  - Baz: baz.md\n  - Borgs:\n    - Bar: borgs/bar.md\n    - Foo: borgs/foo.md\n```\n\n</td></tr><tr>\n<td>and the file <b>borgs/SUMMARY.md</b>:</td>\n</tr><tr><td>\n\n```markdown\n* [Bar](bar.md)\n* [Foo](foo.md)\n```\n\n</td></tr></table>\n\nOr perhaps you don\'t care about the order of the pages under the borgs/ directory? Just drop the file <b>borgs/SUMMARY.md</b> and let it be inferred.\n\nThe fallback behavior follows the [default behavior of MkDocs when nav isn\'t specified][nav-gen], except that you can opt out on a per-directory basis.\n\n[nav-gen]: https://www.mkdocs.org/user-guide/writing-your-docs/#configure-pages-and-navigation\n\nIs your directory structure not so tidy? That\'s not a problem, the implicit nav will not add duplicates of pages already mentioned elsewhere (but you can always add duplicates explicitly...)\n\n#### `nav_file`\n\nWe\'ve been using **SUMMARY.md** as the name of the file that specifies the nav, but naturally, you can use any other file name. The plugin takes care to not let MkDocs complain if you don\'t end up using the nav document as an actual page of your doc site.\n\nOr maybe you want the opposite -- make the nav page very prominent? You can actually use the index page, **README.md**, for the nav (and that\'s even the default)! Why would one do this? Well, GitHub (or another source hosting) also displays the Markdown files, and it\'s quite a nice perk to show off your navigation right in the index page of a directory. What\'s that, you ask? If the index page is taken up by navigation, we can\'t put any other content there, can we? Actually, we can! The nav list can just be put at the bottom of the page that also has whatever other content before that.\n\n#### Explicit nav mark\n\nIf the plugin is confused where on the page the nav is, please precede the Markdown list with this HTML comment (verbatim) on a line of its own:\n\n```markdown\n<!--nav-->\n```\n\n### Migrating from GitBook?\n\nIt might be very easy! Just beware of the stricter Markdown parser; it will *not* accept 2-space indentation for sub-lists.\n\nAnd use this for **mkdocs.yml**:\n\n<table><tr><td>\n\n```yaml\nuse_directory_urls: false\n```\n```yaml\nplugins:\n  - search\n  - same-dir\n  - section-index\n  - literate-nav:\n      nav_file: SUMMARY.md\n```\n\n</td><td>\n\n```yaml\ntheme:\n  name: material\n```\n```yaml\nmarkdown_extensions:\n  - pymdownx.highlight\n  - pymdownx.magiclink\n  - pymdownx.superfences\n```\n\n</td></tr></table>\n',
    'author': 'Oleh Prypin',
    'author_email': 'oleh@pryp.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oprypin/mkdocs-literate-nav',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
