import sqlite3
import alpaca_trade_api as tradeapi

connection = sqlite3.connect('app.db')

cursor = connection.cursor()

# cursor.execute("INSERT INTO stock (symbol, company) VALUES ('ADBE', 'Adobe Inc.')")
# cursor.execute("INSERT INTO stock (symbol, company) VALUES ('VZ', 'Verizon')")
# cursor.execute("INSERT INTO stock (symbol, company) VALUES ('Z', 'Zillow')")

# cursor.execute("DELETE FROM stock")

api = tradeapi.REST('PKWZU1MUM5DDQJ0MCJII',
                    'p2tpKxppRP3uJlNmG4X6vNcaWziD7LNUXba1mbby',
                    base_url='https://paper-api.alpaca.markets')

assets = api.list_assets()

for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable:
            cursor.execute("INSERT INTO stock (symbol, company) VALUES (?, ?)", (asset.symbol, asset.name))
    except Exception as e:
        print(asset.symbol)
        print(e)

connection.commit()