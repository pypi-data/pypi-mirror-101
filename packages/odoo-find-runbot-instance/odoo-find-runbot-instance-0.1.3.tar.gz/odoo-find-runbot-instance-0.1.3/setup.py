# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odoo_find_runbot_instance']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0']

entry_points = \
{'pytest11': ['odoo-find-runbot-instance = '
              'odoo_find_runbot_instance.pytest_fixtures']}

setup_kwargs = {
    'name': 'odoo-find-runbot-instance',
    'version': '0.1.3',
    'description': 'Find and return url, database and user credentials of a live Odoo instance running on the runbot',
    'long_description': '## Introduction\n\nThis package can be used by Odoo devs looking to test their integration/RPC code against a safe/sandbox live Odoo instance.\n\nThe runbot servers offer many such instances, which this module can access to find and return url, database and user credentials\nof some of these live instances.\n\nTry to be light with your tests, do not abuse Odoo\'s runbot servers.\n\nBelow some basic usage examples, but do take a look at the code to see some other useful methods.\n\n\n## Usage \n\n####1. Simple example, using default values:\n\n```python\nfrom odoo_find_runbot_instance import get_runbot_url_db, runbot_admin_user_credentials\nimport httpx\n\nurl, db = get_runbot_url_db(httpx)\nusername, passwd = runbot_admin_user_credentials()\n```\n---\n####2. Same, but for version 14 and enterprise branch:\n\n```python\nfrom odoo_find_runbot_instance import get_runbot_url_db, runbot_admin_user_credentials\nimport httpx\n\nurl, db = get_runbot_url_db(httpx, version=\'14.0\', branch=\'enterprise\')\nusername, passwd = runbot_admin_user_credentials()\n```\n----\n\n## Pytest Usage\n\n\n###conftest.py\n\n---\n```python\nimport pytest\nimport httpx\nfrom typing import Tuple\nfrom odoo_find_runbot_instance import runbot_admin_user_credentials, get_runbot_url_db\n\n\n@pytest.fixture(scope=\'package\')\ndef url_db_user_pwd() -> Tuple[str, str, str, str]:\n    username, password = runbot_admin_user_credentials()\n    # if you prefer to use the demo user use the line below\n    # username, password = runbot_admin_user_credentials()\n    url, db = get_runbot_url_db(httpx)\n    return f"{url}/jsonrpc", db, username, password\n```\n---\n\n\n### test_example.py\n\n---\n```python\nimport httpx\nfrom aio_odoorpc import OdooRPC\n\n\ndef test_odoo(url_db_user_pwd: list):\n    url, db, user, pwd = url_db_user_pwd\n \n    with httpx.Client() as session:\n        odoo = OdooRPC(database=db,\n                       username_or_uid=user,\n                       password=pwd,\n                       http_client=session,\n                       url_jsonrpc_endpoint=url,\n                       default_model_name=\'product.template\')\n        odoo.login()\n        # you are all set...\n        products = odoo.search_read(domain=[], fields=[\'list_price\'], limit=10)\n        ...\n```\n---\n',
    'author': 'mbello',
    'author_email': 'mbello@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mbello/odoo-find-runbot-instance',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
