import pytest
from typing import Tuple
from odoo_find_runbot_instance import \
    runbot_admin_user_credentials, \
    runbot_unpriv_user_credentials, \
    get_runbot_url_db


@pytest.fixture(scope='session')
def version():
    return None


@pytest.fixture(scope='session')
def branch():
    return None


@pytest.fixture(scope='session')
def runbot_url_db(http_client, version, branch) -> Tuple[str, str, str]:
    kwargs = {'http_client': http_client}
    if version is not None:
        kwargs['version'] = version
    if branch is not None:
        kwargs['branch'] = branch
    url, db = get_runbot_url_db(**kwargs)
    return url, f"{url}{'' if url.endswith('/') else '/'}jsonrpc", db


@pytest.fixture(scope='session')
def runbot_url_db_user_pwd(http_client, version, branch, runbot_url_db) -> Tuple[str, str, str, str, str]:
    url, url_jsonrpc, db = runbot_url_db
    username, password = runbot_admin_user_credentials()
    return url, url_jsonrpc, db, username, password


@pytest.fixture(scope='session')
def runbot_url_db_user_pwd_unpriv(http_client, version, branch, runbot_url_db) -> Tuple[str, str, str, str, str]:
    url, url_jsonrpc, db = runbot_url_db
    username, password = runbot_unpriv_user_credentials()
    return url, url_jsonrpc, db, username, password
