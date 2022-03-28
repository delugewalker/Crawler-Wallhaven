import requests
from fake_useragent import UserAgent

from components.headers import get_headers
from components.proxies import getProxies
from components.login import login
from components.download import download

from arguments import wallhaven_argparse

ua = UserAgent(use_cache_server=False, path="components/fake_useragent.json")

args = wallhaven_argparse().parse_args()

if __name__ == "__main__":

    session = requests.Session()
    headers = get_headers(ua=ua)
    if args.use_proxy == True:
        proxies = getProxies(proxy=args.proxy, http=False, https=True)
    else:
        proxies = None

    response = session.get(url=args.login_url_get, headers=headers)
    response = login(args=args, response=response, session=session, headers=headers)

    download(
        args=args, response=response, session=session, headers=headers, proxies=proxies
    )
