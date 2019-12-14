import time
from binance.client import Client
from binance.websockets import BinanceSocketManager
from datetime import datetime
from binance.enums import *

from DB import get_db_connection
from crypo import get_pnl, get_user_coin_account, updateUnrealizedNpl

PUBLIC = 'GoqCFbm6eoXLFtqS1Od8LVXO9NVgHq2HMgzq2iRLAnUKWHUsFR0u4KQBSH0Q4Sjq'
SECRET = 'binance-websocket-s'

CURRENT_TIME = {'BTCUSDT': datetime.now().timestamp(),
                'ETHUSDT': datetime.now().timestamp(),
                'LTCUSDT': datetime.now().timestamp()}


def parse_timestamp(timestamp):
    timestamp = timestamp / 1000

    new_time = datetime.fromtimestamp(timestamp)

    new_time.strftime('%Y-%m-%d %H:%M:%S')
    return new_time


def handle_message(msg):
    global CURRENT_TIME
    message_time = parse_timestamp(msg['E'])
    symbol = msg['k']['s']

    if msg['E'] > CURRENT_TIME.get(symbol, 0) + 60 * 1000:
        print('Time: {} from: {}, to : {}'.format(message_time, parse_timestamp(msg['k']['t']),
                                                  parse_timestamp(msg['k']['T'])))
        CURRENT_TIME[symbol] = msg['E']
        open = msg['k']['o']
        high = msg['k']['h']
        low = msg['k']['l']
        close = msg['k']['c']
        volume = msg['k']['v']
        try:
            insert_into_database(TickerPrice(symbol, message_time, open, high, low, close, volume))
        except:
            print('problem')


def steamming(symbol, seconds):
    # Instantiate a Client
    client = Client(api_key=PUBLIC, api_secret=SECRET)

    bm = BinanceSocketManager(client)

    conn_key = bm.start_kline_socket(symbol, handle_message, interval=KLINE_INTERVAL_1MINUTE)
    # then start the socket manager
    bm.start()

    # let some data flow..
    time.sleep(seconds)

    # stop the socket manager
    bm.stop_socket(conn_key)


def insert_into_database(ticker):
    db = get_db_connection()
    sql = '''
    INSERT INTO `MASY`.`marketplace`
(`symbol`,
`real_time`,
`open_pr`,
`high_pr`,
`low_pr`,
`close_pr`,
`volume`)
VALUES
('{symbol}','{real_time}',{open_pr},{high_pr},{low_pr},{close_pr},{volume});
    '''.format(symbol=ticker.symbol[:3], real_time=ticker.time, open_pr=ticker.open,
               low_pr=ticker.low, high_pr=ticker.high, close_pr=ticker.close, volume=ticker.volume)
    cur = db.cursor()

    cur.execute(sql)
    db.commit()
    db.close()
    cur.close()

    update_unrealized_npl(ticker.symbol[:3], float(ticker.close))


def update_unrealized_npl(symbol, price):
    userCoinAccount = get_user_coin_account()
    coin_quantity = userCoinAccount.map[symbol][0]
    coin_vwp = userCoinAccount.map[symbol][1]
    unrealized_pnl = (price - coin_vwp) * coin_quantity
    updateUnrealizedNpl(symbol, unrealized_pnl)


def load_last_day_klines():
    symbols = ['BTCUSDT', 'ETHUSDT', 'LTCUSDT']
    client = Client(api_key=PUBLIC, api_secret=SECRET)

    for symbol in symbols:

        for kline in client.get_historical_klines_generator(symbol, Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC"):
            timestamp = kline[0]
            time = parse_timestamp(timestamp)
            open = kline[1]
            high = kline[2]
            low = kline[3]
            close = kline[4]
            volume = kline[5]
            try:
                insert_into_database(TickerPrice(symbol[:3], time, open, high, low, close, volume))
            except:
                print('ok')


class TickerPrice:

    def __init__(self, symbol, time, open, high, low, close, volume):
        self.symbol = symbol
        self.time = time
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

    def __str__(self) -> str:
        return '{sysbom}, {time}'.format(self.symbol, self.time)
