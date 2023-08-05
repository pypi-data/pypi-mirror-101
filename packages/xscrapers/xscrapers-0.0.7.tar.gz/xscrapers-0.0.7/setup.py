# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xscrapers', 'xscrapers.tools']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'fake-useragent>=0.1.11,<0.2.0',
 'html5lib>=1.1,<2.0',
 'numpy>=1.20.2,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'selenium>=3.141.0,<4.0.0']

setup_kwargs = {
    'name': 'xscrapers',
    'version': '0.0.7',
    'description': 'A simple webscraper library',
    'long_description': '# XSCRAPERS\n\nThe [XSCRAPERS](https://github.com/juliandwain/webscrapers) package provides an OOP interface to some simple webscraping techniques.\n\nA base use case can be to load some pages to [Beautifulsoup Elements](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).\nThis package allows to load the URLs concurrently using multiple threads, which allows to safe an enormous amount of time.\n\n```python\nimport xscrapers.webscraper as ws\n\nURLS = [\n    "https://www.google.com/",\n    "https://www.amazon.com/",\n    "https://www.youtube.com/",\n]\nPARSER = "html.parser"\nweb_scraper = ws.Webscraper(PARSER, verbose=True)\nweb_scraper.load(URLS)\nweb_scraper.parse()\n\n```\n\nNote that herein, the data scraped is stored in the `data` attribute of the webscraper.\nThe URLs parsed are stored in the `url` attribute.\n\n## Downloading the Firefox Geckodriver\n\n### Linux\n\nSee [this link](https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu) for a good explanation.\nIn short, the steps are:\n\n1. Download the geckodriver from the [mozilla GitHub release page](https://github.com/mozilla/geckodriver/releases), note to change the `X` for the version you want to download\n\n    ```properties\n    wget https://github.com/mozilla/geckodriver/releases/download/vX.XX.X/geckodriver-vX.XX.X-linux64.tar.gz\n    ```\n\n2. Extract the file with\n\n    ```properties\n    tar -xvzf geckodriver*\n    ```\n\n3. Make it executable\n\n    ```properties\n    chmod +x geckodriver\n    ```\n\n4. In the last step, the driver can be added to the `PATH` environment variable, moved to the `usr/local/bin` folder, or can be given as full path to the `Webdriver` class as `exe_path` argument\n\n    ```properties\n    export PATH=$PATH:/path-to-extracted-file/\n    sudo mv geckodriver /usr/local/bin/\n    ```\n',
    'author': 'Julian Stang',
    'author_email': 'julian.stang@tum.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/juliandwain/xscrapers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
