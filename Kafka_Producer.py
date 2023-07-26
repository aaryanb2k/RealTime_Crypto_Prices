import os 
import pandas as pd
from datetime import  datetime
from kafka import KafkaProducer
from json import dumps
import time
from csv import DictReader
import logging
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': os.environ.get('API_Token'),
}

session = Session()
session.headers.update(headers)

class Producer:
    producer = KafkaProducer(bootstrap_servers=["localhost:9092"],value_serializer = lambda x:dumps(x).encode('utf-8'))
    topic = 'Popular_Crypto'

    def send_data(self,data):
        self.producer.send(self.topic,value=data)
        print(data)


if __name__ == "__main__":
    try:
        prod = Producer()
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        while True:
            for i in data['data']:
                if i['name'] in ('Bitcoin','Ethereum','Tether','Binance Coin','XRP','Cardano','Solana','Polkadot','Litecoin','Avalanche','Dogecoin'):
                    x = {'id':i['id'],'name':i['name'],'symbol':i['symbol'],'date_added':i['date_added'],'price':i['quote']['USD']['price'],'last_updated':i['quote']['USD']['last_updated'],'volume_24h':i['quote']['USD']['volume_24h'],'market_cap':i['quote']['USD']['market_cap']}
                    prod.send_data(x)
            time.sleep(2)
            
    except Exception as e:
        print(e)



