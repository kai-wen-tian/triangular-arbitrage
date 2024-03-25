import json
import ccxt

with open('triangular_relationships.json', 'r') as file:
    data = json.load(file)

exchange = ccxt.binance()

counter=0

for relationship in data['triangular_relationships']:
    try:
        pair1 = relationship[0]
        pair2 = relationship[1]
        pair3 = relationship[2]

        ticker1 = exchange.fetch_ticker(pair1)
        ticker2 = exchange.fetch_ticker(pair2)
        ticker3 = exchange.fetch_ticker(pair3)

        pair1_bid = exchange.fetch_order_book(pair1)['bids'][0][0]
        pair1_ask = exchange.fetch_order_book(pair1)['asks'][0][0]
        pair2_bid = exchange.fetch_order_book(pair2)['bids'][0][0]
        pair2_ask = exchange.fetch_order_book(pair2)['asks'][0][0]
        pair3_bid = exchange.fetch_order_book(pair3)['bids'][0][0]
        pair3_ask = exchange.fetch_order_book(pair3)['asks'][0][0]

        fee_percentage_pair1 = 0 
        fee_percentage_pair2 = 0.075
        fee_percentage_pair3 = 0

        pair1_buy_price = pair1_ask
        pair1_sell_price = pair1_bid

        coinA = 1000 / pair1_buy_price

        pair2_buy_price = pair2_ask
        pair2_sell_price = pair2_bid

        coin1=pair1.split("/")
        coin2=pair2.split("/")

        if(coin1[0] == coin2[0]):
            coinB = (coinA * pair2_sell_price) * (100 - fee_percentage_pair2) / 100
        elif (coin1[0] == coin2[1]):
            coinB = (coinA /pair2_buy_price) * (100 - fee_percentage_pair2) / 100


        pair3_buy_price = pair3_ask
        pair3_sell_price = pair3_bid

        coinc = (coinB * pair3_sell_price)
        if coinc>1000:
            print("Trade Found")
            print(f"Triangular relationship: {pair1} -> {pair2} -> {pair3}")
            print("A", coinA)
            print("B",coinB)
            print("C",coinc)
    except:
        counter=counter+1
        print(counter, " Error skipped")

