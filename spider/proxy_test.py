# coding:utf8
import requests
from random import choice

proxies = [
	{'http': 'http://45.79.217.88:3128'},
	# {'http': 'http://xx.xx.xx.xx:xx'},
	# {'http': 'http://user:pass@host:port'}
]

url = 'http://www.baidu.com'
response = requests.get(url, proxies=choice(proxies))

print response.status_code
