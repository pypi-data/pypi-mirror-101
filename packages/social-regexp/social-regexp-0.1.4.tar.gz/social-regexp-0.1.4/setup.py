# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['social_regexp']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6,<4.0']}

setup_kwargs = {
    'name': 'social-regexp',
    'version': '0.1.4',
    'description': 'Regexps for social data',
    'long_description': '# social-regexp\n\n<div align="center">\n\n[![Build status](https://github.com/TezRomacH/social-regexp/workflows/build/badge.svg?branch=master&event=push)](https://github.com/TezRomacH/social-regexp/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/social-regexp.svg)](https://pypi.org/project/social-regexp/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/TezRomacH/social-regexp/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/TezRomacH/social-regexp/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/TezRomacH/social-regexp/releases)\n[![License](https://img.shields.io/github/license/TezRomacH/social-regexp)](https://github.com/TezRomacH/social-regexp/blob/master/LICENSE)\n\nRegexps for social data\n\n</div>\n\n## Installation\n\n```bash\npip install -U social-regexp\n```\n\n## Methods\n\n```python\n>>> import social_regexp as sre\n>>> text = "Hi, my Twitter is @tez_romach"\n\n>>> sre.remove_mentions(text, sre.MENTION_TOKEN)\n"Hi, my Twitter is <men>"\n```\n\nFull list of methods available here:\n\n```python\n\ndef not_contains_non_russian_cyrillic_letters(text: str) -> bool:\n    """Checks if a text contains any non-russian but cyrillic letter."""\n\ndef url() -> Pattern[str]:\n    """Returns a pattern to match URLs."""\n\n\ndef spaces_before_punctuation() -> Pattern[str]:\n    """Returns a pattern to match spaces before punctuation."""\n\ndef single_letter_words() -> Pattern[str]:\n    """Returns a pattern to match single letter words."""\n\ndef blank_spaces() -> Pattern[str]:\n    """Returns a pattern to match blank spaces."""\n\ndef mentions() -> Pattern[str]:\n    """Returns a pattern to match mentions from Twitter or Instagram."""\n\ndef phones() -> Pattern[str]:\n    """Returns a pattern to match phone numbers."""\n\ndef remove_urls(text: str, repl: str = "") -> str:\n    """Return new string with replaced URLs to `repl`."""\n\ndef remove_spaces_before_punctuation(text: str) -> str:\n    """Return new string without spaces before punctuations."""\n\ndef remove_punctuation(text: str) -> str:\n    """Return new string without punctuations."""\n\ndef remove_mentions(text: str, repl: str = "") -> str:\n    """Return new string with replaced Twitter/Instagram mentions to `repl`."""\n\ndef remove_single_letter_words(text: str) -> str:\n    """Return new string without single-letter words."""\n\ndef remove_blank_spaces(text: str) -> str:\n    """Return new string without blank spaces."""\n\ndef remove_phones(text: str, repl: str = "") -> str:\n    """Return new string with replaced phone numbers to `repl`."""\n\ndef preprocess_text(text: str) -> str:\n    """Return new string with tokenized and processed text."""\n    result = remove_mentions(text, repl=MENTION_TOKEN)\n    result = remove_phones(result, repl=PHONE_TOKEN)\n    result = remove_urls(result, repl=URL_TOKEN)\n    result = remove_blank_spaces(result).strip()\n    result = remove_spaces_before_punctuation(result)\n\n    return result\n```\n\n## Constants\n\n```python\nMENTION_TOKEN = "<men>"\nURL_TOKEN = "<url>"\nPHONE_TOKEN = "<phn>"\nHASH_TOKEN = "<hsh>"\n\nALL_TOKENS = [MENTION_TOKEN, URL_TOKEN, PHONE_TOKEN, HASH_TOKEN]\n\nNON_RUSSIAN_CYRILLIC_LETTERS = {\n    "ә", "җ", "ң", "ө", "ү",\n    "қ", "ӯ", "ҳ", "ҷ", "ғ",\n    "ұ", "ә", "һ", "ґ", "є",\n    "ї", "ӑ", "ӗ", "ҫ", "ӳ",\n    "ҝ", "ғ", "ҹ",\n}\n```\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/TezRomacH/social-regexp)](https://github.com/TezRomacH/social-regexp/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/TezRomacH/social-regexp/blob/master/LICENSE) for more details.\n\n## 📃 Citation\n\n```\n@misc{social-regexp,\n  author = {TezRomacH},\n  title = {Regexps for social data},\n  year = {2021},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/TezRomacH/social-regexp}}\n}\n```\n\n## Credits\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template).\n',
    'author': 'TezRomacH',
    'author_email': 'tez.romach@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TezRomacH/social-regexp',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
