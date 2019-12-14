from DB import get_db_connection
import collections


def get_latest_price(symbol):
    db = get_db_connection()
    cur = db.cursor()
    sql = '''
    select close_pr from marketplace where symbol = '{symbol}' and real_time =
    (select max(real_time) from marketplace where symbol = '{symbol}') '''.format(symbol=symbol)

    cur.execute(sql)

    price = cur.fetchone()

    db.commit()
    cur.close()
    db.close()
    return price[0]


def get_all_blotter():
    db = get_db_connection()
    cur = db.cursor()
    sql = '''
    SELECT `blotter`.`real_time`,
    `blotter`.`coin`,
    `blotter`.`quantity`,
    `blotter`.`price`,
    `blotter`.`buy_sell`
    FROM `MASY`.`blotter` order by `blotter`.`real_time` desc;
           '''

    cur.execute(sql)

    all = cur.fetchall()
    db.commit()
    cur.close()
    db.close()

    return [(ele[0].strftime('%Y-%m-%d %H:%M:%S'), ele[1], ele[2], ele[3], ele[4]) for ele in all]


def insert_into_blotter(coin, qty, price, side):
    db = get_db_connection()
    cur = db.cursor()
    sql = '''
       INSERT INTO `MASY`.`blotter`
        (`real_time`,
        `coin`,
        `quantity`,
        `price`,
        `buy_sell`)
        VALUES
        (CURRENT_TIMESTAMP,'{coin}',{qty},{price},'{side}') '''.format(coin=coin, qty=qty, price=price, side=side)

    cur.execute(sql)
    db.commit()
    cur.close()
    db.close()


def get_user_account():
    db = get_db_connection()
    cur = db.cursor()
    sql = '''
       SELECT full_name, cash_availble FROM `MASY`.`users`; '''

    cur.execute(sql)
    user = cur.fetchone()
    db.commit()
    cur.close()
    db.close()
    return User(user[0], user[1])


def updateCoin(coin, total_number, vwp):
    db = get_db_connection()
    cur = db.cursor()
    sql = '''
        UPDATE `MASY`.`user_coin_account`
        SET
        `number` = {number},
        `vwp` = {vwp}
        WHERE `coin` = '{coin}'; '''.format(number=total_number, coin=coin, vwp=vwp)

    cur.execute(sql)
    db.commit()
    cur.close()
    db.close()


def updateMoney(number):
    db = get_db_connection()
    cur = db.cursor()
    sql = '''
        update `MASY`.`users` set `cash_availble` = {number}; '''.format(number=number)

    cur.execute(sql)
    db.commit()
    cur.close()
    db.close()


def get_pnl(coin):
    db = get_db_connection()
    cur = db.cursor()
    sql = '''select realized_pnl,unrealized_pnl from `MASY`.`pnl` where `coin`='{coin}' '''.format(coin=coin)

    cur.execute(sql)
    res = cur.fetchone()
    db.commit()
    cur.close()
    db.close()
    return [float(i) for i in res]


def get_all_coins_pnl():
    db = get_db_connection()
    cur = db.cursor()
    sql = '''select coin, realized_pnl,unrealized_pnl from `MASY`.`pnl` '''

    cur.execute(sql)
    res = cur.fetchall()
    db.commit()
    cur.close()
    db.close()
    return res


def updateRealizedNpl(coin, money):
    db = get_db_connection()
    cur = db.cursor()
    sql = '''
            update `MASY`.`pnl` set `realized_pnl` = {number}, `timestamp` = CURRENT_TIMESTAMP where `coin`='{coin}'; ''' \
        .format(number=money, coin=coin)

    cur.execute(sql)
    db.commit()
    cur.close()
    db.close()


def updateUnrealizedNpl(coin, money):
    db = get_db_connection()
    cur = db.cursor()
    sql = '''
            update `MASY`.`pnl` set `unrealized_pnl` = {number}, `timestamp` = CURRENT_TIMESTAMP where `coin`='{coin}'; ''' \
        .format(number=money, coin=coin)

    cur.execute(sql)
    db.commit()
    cur.close()
    db.close()


# updateMoney(200000)
# updateCoin('BTC',1,1000)

def get_user_coin_account():
    db = get_db_connection()
    cur = db.cursor()
    sql = '''
       SELECT coin,number,vwp FROM MASY.user_coin_account; '''

    cur.execute(sql)
    all_information = cur.fetchall()
    account = UserCoinAccount()
    for info in all_information:
        account.add(info[0], info[1], info[2])

    db.commit()
    cur.close()
    db.close()
    return account


class UserCoinAccount:

    def __init__(self):
        self.map = collections.defaultdict(list)

    def add(self, coin, number, vwp):
        if coin not in self.map:
            self.map[coin] = [0, 0]

        if self.map[coin][0] + number == 0:
            self.map[coin] = [0, 0]
            return
        self.map[coin] = (self.map[coin][0] + number,
                          (number * vwp + self.map[coin][1] * self.map[coin][0]) / (self.map[coin][0] + number))


class User:
    def __init__(self, name, cash):
        self.name = name
        self.cash = cash
