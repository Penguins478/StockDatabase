import config
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST, TimeFrame
import sqlite3

api = tradeapi.REST(config.API_KEY,
                    config.SECRET_KEY,
                    base_url=config.BASE_URL)

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
cursor.execute("""
    SELECT id, symbol, company FROM stock
""")
rows = cursor.fetchall()
symbols = []
stock_dict = {}
# for each stock symbol, append to array symbols and for each symbol set its value to the its stock id
for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']

chunk_size = 200
for i in range(0, len(symbols), chunk_size):
    symbol_chunk = symbols[i:i+chunk_size]
        
    barsets = api.get_bars_iter(symbol_chunk, TimeFrame.Day, "2022-03-31", "2022-04-02")

for bar in barsets:
        symbol = bar.S
        stock_id = stock_dict[symbol]
        print(f'processing symbol', symbol)

        cursor.execute("""
            INSERT INTO stock_price (stock_id, date, open, high, low, close, volume, number_of_trades, volume_weighted_average_price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v, bar.n, bar.vw))
        connection.commit()