#!/usr/bin/env python3
# The following script  is from here: https://linuxhit.com/how-to-easily-get-bitcoin-price-quotes-in-python/
import requests
response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
data = response.json()
# print(data["bpi"]["USD"]["rate"])
