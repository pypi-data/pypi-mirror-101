# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yomidict']

package_data = \
{'': ['*']}

install_requires = \
['EbookLib>=0.17.1,<0.18.0',
 'fugashi>=1.1.0,<2.0.0',
 'srt>=3.4.1,<4.0.0',
 'unidic>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'yomidict',
    'version': '0.1.3',
    'description': 'Create frequency dictionaries for yomichan out of media',
    'long_description': '# yomidict\nCreate frequency dictionaries for yomichan out of media.\\\nCurrently supported formats are: epub, html, srt, txt\n\n```python\npip install yomidict\n```\n\n\nMWE:\n```python\nimport yomidict\ndm = yomidict.DictMaker()\nfilelist = ["test.html"]*5 + ["test.epub"]*2 + ["test.srt"]*2\ndm.feed_files(filelist)\ndm.save("zipfile.zip", "name_in_yomichan")\n```',
    'author': 'exc4l',
    'author_email': 'cps0537@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/exc4l/yomidict',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
