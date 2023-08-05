# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['android_resources_checker']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'rich>=10.0.0,<11.0.0']

entry_points = \
{'console_scripts': ['android-resources-checker = '
                     'android_resources_checker:main']}

setup_kwargs = {
    'name': 'android-resources-checker',
    'version': '0.0.7',
    'description': 'Check if your android resources are being unused.',
    'long_description': '# Android Resources Checker\n\n\n[![Flake8](https://img.shields.io/badge/codestyle-flake8-yellow)](https://flake8.pycqa.org/en/latest/)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Coverage](https://codecov.io/gh/fabiocarballo/android-resources-checker/branch/master/graph/badge.svg)](https://codecov.io/gh/fabiocarballo/android-resources-checker)\n[![License](https://img.shields.io/github/license/fabiocarballo/android-resources-checker)](https://choosealicense.com/licenses/mit)\n\n## What\n\nThis program will inspect the resources of your app and help you understand which ones are not being used and could\npotentially be removed.\n\nMain features:\n\n- Identify the unused resources in your android project.\n- Identify the unused resources in your android library (when you have a multi-repo setup)\n- Listing of the unused resources (name, type and size)\n- Deletion of the unused resources\n\n## Installing\n\nThis program requires Python, supporting from 3.8.x and 3.9.x\n\nIn order to install run:\n\n```shell\npip install -U android-resources-checker\n```\n\n## Using\n\n## Inspecting your app resources.\n\nImagining your app in the project `subject-app`, you can trigger the resources inspection by running:\n\n```shell\nandroid-resources-checker --app /path/to/subject-app\n```\n\n## Inspecting your library app resources.\n\nIn the case you have two projects in separate repos, where a `client-app` depends on a `lib-app`, you can check the unused\nresources of the library app by running:\n\n```shell\nandroid-resources-checker \\\n  --app /path/to/lib-app \\\n  --client /path/to/client-app-1 \\\n  --client /path/to/client-app-2\n```\n\nAn example of a run could look like this:\n\n![](.github/assets/example-terminal.png)\n\n## Reports\n\nThe default report will be always be displayed in your stdout.\n\nYou can specify an optional directory where to write the reports in the form of CSV files. For that use the `--reports-dir` \noption.\n\nFor example:\n\n```shell\nandroid-resources-checker \\\n  --app /path/to/app \\ \n  --reports-dir /path/to/reports\n```\n## License\n\n```\nCopyright (c) 2021 Dotanuki Labs, Fabio Carballo\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of\nthis software and associated documentation files (the "Software"), to deal in\nthe Software without restriction, including without limitation the rights to\nuse, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of\nthe Software, and to permit persons to whom the Software is furnished to do so,\nsubject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS\nFOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR\nCOPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER\nIN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN\nCONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n```\n\n\n\n\n',
    'author': 'Fabio Carballo',
    'author_email': 'fabio.og.carballo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fabiocarballo/android-resources-checker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
