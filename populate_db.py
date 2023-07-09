import sqlite3
import alpaca_trade_api as tradeapi
import config

''' 
Made a scheduler that runs this file at a certain time.

I used "30 4 * * * /opt/homebrew/bin/python3 /Users/ryan/Desktop/StockTradingApp/populate_db.py >> /Users/ryan/Desktop/StockTradingApp/populate.log 2>&1"
to dump all print output from populate_db.py (like adding new stocks ___) into populate.log every day at 4:30am (https://crontab.guru/). I put that line into my cron using
crontab -e. I also had to give full disk access to cron (https://medium.com/vunamhung/granting-full-disk-access-to-cron-29d2267fbe62) so python3 could
open the files. You may also have to say "chmod +rx /Users/ryan/Desktop/StockTradingApp/populate_db.py" if errors still persist.

'''

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

# cursor.execute("INSERT INTO stock (symbol, company) VALUES ('ADBE', 'Adobe Inc.')")
# cursor.execute("INSERT INTO stock (symbol, company) VALUES ('VZ', 'Verizon')")
# cursor.execute("INSERT INTO stock (symbol, company) VALUES ('Z', 'Zillow')")

# cursor.execute("DELETE FROM stock")

cursor.execute("""
    SELECT symbol, company FROM stock
""")

rows = cursor.fetchall()

symbols = [row['symbol'] for row in rows]
# print(symbols)

api = tradeapi.REST(config.API_KEY,
                    config.SECRET_KEY,
                    base_url=config.BASE_URL)

assets = api.list_assets()

for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            print(f"Added a new stock {asset.symbol} {asset.name}")
            cursor.execute("INSERT INTO stock (symbol, company) VALUES (?, ?)", (asset.symbol, asset.name))
    except Exception as e:
        print(asset.symbol)
        print(e)

connection.commit()

