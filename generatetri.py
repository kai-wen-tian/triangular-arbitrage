import ccxt
import json

exchange = ccxt.binance()

markets = exchange.load_markets()

triangular_relationships = []
exclude_currencies=['FDUSD','USDT','BUSD','AUD','EUR','GBP','PLN','RON','TRY','UAH','VND','ZAR','BULL','BEAR']
for pair1 in markets:
    currencies1 = pair1.split('/')
    if 'FDUSD' in currencies1:
        for pair2 in markets:
            currencies2 = pair2.split('/')
            if pair1 != pair2 and all(currency not in currencies2 for currency in exclude_currencies) and any(currency in currencies2 for currency in currencies1 if currency not in exclude_currencies):
                for pair3 in markets:
                    if pair3 != pair2 and pair3 != pair1:
                        currencies3 = pair3.split('/')
                        if (currencies3[0] == currencies1[0] and currencies3[1] == currencies2[0]) or \
                           (currencies3[0] == currencies1[0] and currencies3[1] == currencies2[1]) or \
                           (currencies3[0] == currencies1[1] and currencies3[1] == currencies2[0]) or \
                           (currencies3[0] == currencies1[1] and currencies3[1] == currencies2[1]) or \
                           (currencies3[0] == currencies2[0] and currencies3[1] == currencies1[0]) or \
                           (currencies3[0] == currencies2[0] and currencies3[1] == currencies1[1]) or \
                           (currencies3[0] == currencies2[1] and currencies3[1] == currencies1[0]) or \
                           (currencies3[0] == currencies2[1] and currencies3[1] == currencies1[1]):
                               triangular_relationships.append((pair1, pair2, pair3))

output_data = {"triangular_relationships": triangular_relationships}

if triangular_relationships:
    print("Triangular relationships found:")
    with open('triangular_relationships.json', 'w') as json_file:
        json.dump(output_data, json_file, indent=4)
else:
    print("No triangular relationships found.")
