import requests
from lxml.html import fromstring

from itertools import cycle
import traceback

def get_proxies():
    """
    This function generates random proxies and returns a set of proxies.
    """
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:20]:
        if i.xpath('.//td[7][contains(text(),"yes")]') and i.xpath('.//td[5][contains(text(),"elite proxy")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


proxies = get_proxies()
proxy_pool = cycle(proxies)
print(proxies)
print()
url = 'https://httpbin.org/ip'

for i in range(1,11):
    #Get a proxy from the pool
    proxy = next(proxy_pool)
    proxies = {"http": 'http://'+proxy, "https": 'http://'+proxy}
    print(proxies)
    print("Request #%d"%i)
    try:
        response = requests.get(url,proxies=proxies)
        print(response.json())
    except:
        #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
        #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
        print("Skipping. Connnection error")