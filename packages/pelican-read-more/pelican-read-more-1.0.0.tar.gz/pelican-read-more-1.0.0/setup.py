# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.read_more']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.0', 'pelican>=4.5']

extras_require = \
{'markdown': ['markdown>=3.2.2']}

setup_kwargs = {
    'name': 'pelican-read-more',
    'version': '1.0.0',
    'description': 'Pelican plugin that adds an inline “Read More…” link',
    'long_description': 'Read More: A Plugin for Pelican\n===============================\n\n[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/read-more/build)](https://github.com/pelican-plugins/read-more/actions)\n[![PyPI Version](https://img.shields.io/pypi/v/pelican-read-more)](https://pypi.org/project/pelican-read-more/)\n![License](https://img.shields.io/pypi/l/pelican-read-more?color=blue)\n\nThis Pelican plugin inserts an inline “Read More” link into the last HTML element of the summary.\n\nFor more information regarding why it was created, please visit: https://www.vuongnguyen.com/read-more-python-lxml/\n\nInstallation\n------------\n\nThis plugin can be installed via:\n\n    python -m pip install pelican-read-more\n\nSettings\n--------\n\nThe following settings are available. If not set, the plugin will use default values.\n\nThe following setting defines the string that is added to the end of the summary, before the “Read More” link:\n\n\tSUMMARY_END_SUFFIX = "..."\n\nThe following setting defines the summary length before truncating and adding the “Read More” link:\n\n    SUMMARY_MAX_LENGTH = 50\n\nThe following setting defines the “Read More” link text:\n\n    READ_MORE_LINK = \'<span>continue</span>\'\n\nThe following setting defines the format of the “Read More” link:\n\n    READ_MORE_LINK_FORMAT = \'<a class="read-more" href="/{url}">{text}</a>\'\n\nContributing\n------------\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/pelican-plugins/read-more/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n\nContributors\n------------\n\nContributors include: [Vuong Nguyen](https://www.vuongnguyen.com), Dashie, [Justin Mayer](https://justinmayer.com), Kernc\n\nLicense\n-------\n\nThis project is licensed under the AGPL 3.0 license.\n',
    'author': 'Pelican Dev Team',
    'author_email': 'authors@getpelican.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pelican-plugins/read-more',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
