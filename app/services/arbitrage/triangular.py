
import json
import os
from pathlib import Path
import ccxt
import schedule
import time
import logging
json_file_path = Path(__file__).resolve().parent.parent.parent / 'data' / 'triangular_relationships.json'

with open(json_file_path, 'r') as file:
    data = json.load(file)
def execute_tri():
    print("Running script...")
    json_file_path = Path(__file__).resolve().parent.parent.parent / 'data' / 'triangular_relationships.json'
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    exchange = ccxt.binance()
    def calculate_buy_or_sell(pair1, pair2, coin1, pair2_sell_price, pair2_buy_price, fee_percentage_pair):
        coin_pair1=pair1.split("/")
        coin_pair2=pair2.split("/")
        if coin_pair1[0] == coin_pair2[0]:
            coin2 = (coin1 * pair2_sell_price) * (100 - fee_percentage_pair) / 100
        elif coin_pair1[0] == coin_pair2[1]:
            coin2 = (coin1 / pair2_buy_price) * (100 - fee_percentage_pair) / 100
        return coin2
    def calculate_profit(pair1, pair2, pair3):
        ticker1 = exchange.fetch_ticker(pair1)
        ticker2 = exchange.fetch_ticker(pair2)
        ticker3 = exchange.fetch_ticker(pair3)
        pair1_sell_price = ticker1['bid']
        pair1_buy_price = ticker1['ask']
        pair2_sell_price = ticker2['bid']
        pair2_buy_price = ticker2['ask']
        pair3_sell_price = ticker3['bid']
        pair3_buy_price = ticker3['ask']
        fee_percentage_pair = 0.075
        quoteCurrency = pair1.split("/")[1]
        if 'ETH' in quoteCurrency or 'BTC' in quoteCurrency:
            pair0 = quoteCurrency + '/FDUSD'
            ticker0 = exchange.fetch_ticker(pair0)
            pair0_sell_price = ticker0['bid']
            pair0_buy_price = ticker0['ask']
            coin0 = (1000 / pair0_buy_price) * (100 - fee_percentage_pair) / 100
            coin1 = calculate_buy_or_sell(pair0, pair1, coin0, pair1_sell_price, pair1_buy_price,
                                           fee_percentage_pair)
            coin2 = calculate_buy_or_sell(pair1, pair2, coin1, pair2_sell_price, pair2_buy_price,
                                          fee_percentage_pair)
            coin3 = (coin2 * pair3_sell_price) * (100 - fee_percentage_pair) / 100
            coin4 = (coin3 * pair0_sell_price) * (100 - fee_percentage_pair) / 100
            return coin4
        else:
            coin1 = (1000 / pair1_buy_price) * (100 - fee_percentage_pair) / 100
            coin2 = calculate_buy_or_sell(pair1, pair2, coin1, pair2_sell_price, pair2_buy_price,
                                          fee_percentage_pair)
            coin3 = (coin2 * pair3_sell_price) * (100 - fee_percentage_pair) / 100
            return coin3
    for relationship in data['triangular_relationships']:
        try:
            pair1 = relationship[0]
            pair2 = relationship[1]
            pair3 = relationship[2]
            coin = calculate_profit(pair1, pair2, pair3)
            if coin > 1000:
                print("Trade Found")
                print(f"Triangular relationship: {pair1} -> {pair2} -> {pair3}")
                print(coin)
                return coin
                break
            else:
                print("Trade Not Found")
                print(f"Triangular relationship: {pair1} -> {pair2}-> {pair3}")
                print(coin)
                #return (coin)
                #break
        except:
            continue
    print("Script finished.")
    
"""
execute_tri()
schedule.every(2).minutes.do(execute_tri)
while True:
    schedule.run_pending()
    time.sleep(1)"""
