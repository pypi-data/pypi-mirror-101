## Introduction

This package can be used by Odoo devs looking to test their integration/RPC code against a safe/sandbox live Odoo instance.

The runbot servers offer many such instances, which this module can access to find and return url, database and user credentials
of some of these live instances.

Try to be light with your tests, do not abuse Odoo's runbot servers.

Below some basic usage examples, but do take a look at the code to see some other useful methods.


## Usage 

####1. Simple example, using default values:

```python
from odoo_find_runbot_instance import get_runbot_url_db, runbot_admin_user_credentials
import httpx

url, db = get_runbot_url_db(httpx)
username, passwd = runbot_admin_user_credentials()
```
---
####2. Same, but for version 14 and enterprise branch:

```python
from odoo_find_runbot_instance import get_runbot_url_db, runbot_admin_user_credentials
import httpx

url, db = get_runbot_url_db(httpx, version='14.0', branch='enterprise')
username, passwd = runbot_admin_user_credentials()
```
----

## Pytest Usage


###conftest.py

---
```python
import pytest
import httpx
from typing import Tuple
from odoo_find_runbot_instance import runbot_admin_user_credentials, get_runbot_url_db


@pytest.fixture(scope='package')
def url_db_user_pwd() -> Tuple[str, str, str, str]:
    username, password = runbot_admin_user_credentials()
    # if you prefer to use the demo user use the line below
    # username, password = runbot_admin_user_credentials()
    url, db = get_runbot_url_db(httpx)
    return f"{url}/jsonrpc", db, username, password
```
---


### test_example.py

---
```python
import httpx
from aio_odoorpc import OdooRPC


def test_odoo(url_db_user_pwd: list):
    url, db, user, pwd = url_db_user_pwd
 
    with httpx.Client() as session:
        odoo = OdooRPC(database=db,
                       username_or_uid=user,
                       password=pwd,
                       http_client=session,
                       url_jsonrpc_endpoint=url,
                       default_model_name='product.template')
        odoo.login()
        # you are all set...
        products = odoo.search_read(domain=[], fields=['list_price'], limit=10)
        ...
```
---
