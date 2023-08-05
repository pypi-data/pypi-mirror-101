from typing import Any, Dict, List, Optional, Tuple
from bs4 import BeautifulSoup
import re


def runbot_admin_user_credentials() -> Tuple[str, str]:
    return 'admin', 'admin'


def runbot_unpriv_user_credentials() -> Tuple[str, str]:
    return 'demo', 'demo'


def runbot_instance_url_to_rpc_url_and_db(lnk: str) -> Tuple[str, str]:
    if lnk.startswith("http:"):
        lnk = f"https{lnk[4:]}"
    m = re.match(r"http[s]?://([\w-]+)\.", lnk)
    
    return lnk, m.group(1)


def scrap_versions(http_client) -> Dict[str, Dict[str, Any]]:
    versions = dict()
    resp = http_client.get(url='http://runbot.odoo.com/runbot')
    soup = BeautifulSoup(resp.text, features='html.parser')
    tags = soup.find_all("a", attrs={'title': 'View Bundle'})
    for t in tags:
        versions[str(t.b.string)] = {"href": str(t.get('href'))}

    return versions


def scrap_batches(http_client,
                  v_dict: Dict[str, Dict[str, Any]],
                  versions: Optional[List[str]] = None,
                  limit: int = 1,
                  success_only: bool = True,
                  runbot_url: str = "https://runbot.odoo.com") -> None:
    
    if not versions:
        versions = v_dict.keys()
    
    for v in versions:
        v = v_dict.get(v)
        batches = list()
        v['batches'] = batches
        if v:
            resp = http_client.get(url=runbot_url + v['href'])
            soup = BeautifulSoup(resp.text, features='html.parser')
            tags = soup.find_all("div", class_="batch_row")
            count: int = 0
            for t in tags:
                st = t.div.find_all('div', class_="bg-success-light" if success_only else "card")
                st = st[0] if st else None
                if not st:
                    continue
                batch = dict()
                batch['href'] = st.find('a', title="View Batch")['href']
                builds = dict()
                batch['builds'] = builds
                bs = st.find_all('div', class_='slot_container')
                for b in bs:
                    lnk = b.find('a', class_='fa-sign-in')
                    if not lnk:
                        continue
                    lnk = lnk['href']
                    build_name = str(b.find('a', class_='slot_name').span.string)
                    builds[build_name] = runbot_instance_url_to_rpc_url_and_db(lnk)
                batches.append(batch)
                count += 1
                if count >= limit:
                    break


def get_runbot_url_db(http_client, version: str = 'master', branch: str = 'odoo') -> Tuple[str, str]:
    v = scrap_versions(http_client)
    scrap_batches(http_client, v, versions=[version], limit=1, success_only=True)
    return v[version]['batches'][0]['builds'][branch]
