import requests, os
from flask import Flask, request, jsonify
from pyairtable import Api
from apscheduler.schedulers.background import BackgroundScheduler
api = Api('patERrR7H1XFtP5eE.82481f7194bff31d0d66ffc33b46a4bf665f5feb4946d2c4f54d446ee81bf61b')
table = api.table('appSIHXEfKMufk452', 'tblC9PqwyrfL5vaQ5')
print(table.all())

cache = []
time = 1
def coin_details_update():
    response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1&sparkline=false&locale=en&precision=2')
    #print(response.json())
    print(cache)
    for i in response.json():
        coin_id = i["id"]
        coin_name = i["name"]
        coin_symbol = i["symbol"]
        coin_current_price = i["current_price"]
        coin_image = i['image']
        coin_market_cap = i['market_cap']
        coin_market_cap_rank = i['market_cap_rank']
        coin_total_supply = i['total_supply']
        table.create({"id": coin_id, "name": coin_name, "symbol": coin_symbol, "current_price":coin_current_price, "image":coin_image,"market_cap":coin_market_cap,"market_cap_rank":coin_market_cap_rank, "total_supply":coin_total_supply})


def current_price_update():
    if (time%10):
        for i in cache:
            coin_id = i['id']
            response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&precision=10')
            i['current_price'] = response.json()[coin_id]['usd']
            print(type(response.json()))
    time += 1


scheduler = BackgroundScheduler()
scheduler.add_job(coin_details_update, 'interval', minutes=10)
scheduler.add_job(current_price_update, 'interval', minutes=1)
coin_details_update()
appl = Flask(__name__)
@appl.route("/coins")
def get_data():
    print(cache)
    return jsonify(cache), 200

@appl.route("/coins/price/<coin_id>}")
def price(coin_id):
    coin_data = []
    for i in cache:
        if i['id'] == coin_id:
            coin_data = [coin_id, i['current_price']]
        # else retrieve from airtable database
    
    return jsonify(coin_data), 200
        
if __name__ == "__main__":
    appl.run(debug=True)