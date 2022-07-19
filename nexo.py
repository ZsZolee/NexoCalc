# The code is from https://gist.github.com/SrNightmare09/c0492a8852eb172ebea6c93837837998

from requests import Request, Session
import json


def getInfo():  # Function to get the info

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'  # Coinmarketcap API url

    parameters = {'slug': 'nexo',
                  'convert': 'USD'}  # API parameters to pass in for retrieving specific cryptocurrency data

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'c970f019-a5e0-49cd-8107-638d432b8300'
    }  # Replace 'YOUR_API_KEY' with the API key you have recieved in the previous step

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)

    info = json.loads(response.text)['data']['2694']['quote']['USD']['price']

    info = (round(float(info), 2))

    return info
