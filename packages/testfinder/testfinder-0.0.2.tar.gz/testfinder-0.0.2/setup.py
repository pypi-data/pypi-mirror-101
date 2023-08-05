# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['testfinder']
entry_points = \
{'console_scripts': ['testfinder = testfinder:main']}

setup_kwargs = {
    'name': 'testfinder',
    'version': '0.0.2',
    'description': 'Find test cases on a Python project.',
    'long_description': '# testfinder - Find tests easier\n\nCommand-line tool to find, print all the test cases in a project.\n\n\n- Find your test methods, class names faster.\n- Integrate with other search/filtering/autocomplete tools like bash, grep, fzf.\n- Defaults to pytest test invocation syntax.\n  -- Other invocation syntax like Django coming soon!\n\n## Install\n\n```shell\npip install testfinder\n```\n\n## Usage\n\n```shell\ncd <project-root>\ntestfinder\n```\n\n### with fzf\n*fzf* is an interactive Unix filter for command-line that can be used with any list and supports fuzzy searches.\n\n- Install [fzf](https://github.com/junegunn/fzf#installation)\n\n\n- Run pytest and find your test\n\n```bash\npytest $(testfinder | fzf)\n```\n\n[![asciicast](https://asciinema.org/a/UxajDsBmyQc0imiiCGzaXd7e8.svg)](https://asciinema.org/a/UxajDsBmyQc0imiiCGzaXd7e8)\n\n# How does it work?\nIn Python the files containing tests usually have the following naming conventions:\n\n- `tests.py`\n- `test_*.py`\n- `*_test.py`\n- `tests/__init__.py`\n\nIt enumerates all the files above, and discovers all the test cases in those files with a few simple regexes.\n',
    'author': 'Sid Mitra',
    'author_email': 'testfinder@sidmitra.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
