from flask import Flask,render_template,request,redirect,flash

from BuySell import BuySellForm
from crypo import get_latest_price, get_user_account, get_user_coin_account, updateCoin, updateMoney, updateRealizedNpl, \
	get_pnl, insert_into_blotter, get_all_blotter, get_all_coins_pnl
from trading import update_unrealized_npl



app = Flask(__name__)

app.secret_key ='test'

UserAccount= get_user_account()
UserCoinAccount=get_user_coin_account()




@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/bank')
def bank():
	return render_template('bank.html')


@app.route('/trade',methods=['GET','POST'] )
def trade_html():
	prices = {'btc_price': get_latest_price('BTC'), 'eth_price': get_latest_price('ETH'),
			  'ltc_price': get_latest_price('LTC')
			  }
	forms = BuySellForm()
	current_holding=UserCoinAccount.map
	return render_template('trade.html', prices=prices, form = forms, current_holding = current_holding)

coins_map = {'1':'BTC','2':'ETH','3':'LTC'}


@app.route('/buysell', methods = ['GET','POST'])
def buySell():
	global  UserAccount,UserCoinAccount

	results = request.form
	cur_coin_quantity = UserCoinAccount.map[coins_map[results['coins']]][0]
	cur_vwp = UserCoinAccount.map[coins_map[results['coins']]][1]
	q = int(results['quantity'])
	coin = coins_map[results['coins']]
	cur_price = get_latest_price(coin)
	transaction_money =  cur_price* q
	side = 'buy' if results['transaction'] == '1' else 'sell'
	if results['transaction'] == '1':
		if UserAccount.cash < transaction_money:
			flash('Error: you don\'t have enough money')
		else:
			new_vwp = (cur_vwp*cur_coin_quantity +q*cur_price)/(q+cur_coin_quantity)
			updateCoin(coin,cur_coin_quantity+q, new_vwp)
			updateMoney(UserAccount.cash-transaction_money)
			insert_into_blotter(coin,q,cur_price,side)
	else:
		if cur_coin_quantity< q:
			flash('Error: you don\'t have enough coin')
		else:
			updateCoin(coin,cur_coin_quantity-q,cur_vwp)
			updateMoney(UserAccount.cash+transaction_money)
			pnl = q*(cur_price-cur_vwp)
			cur_pnl = get_pnl(coin)
			updateRealizedNpl(coin,cur_pnl[0]+pnl)
			update_unrealized_npl(coin, cur_price)

			insert_into_blotter(coin,q,cur_price,side)

	UserAccount = get_user_account()
	UserCoinAccount = get_user_coin_account()

	return redirect('/trade')


@app.route('/pnl')
def pl():
	pnl = get_all_coins_pnl()
	res = []
	for p in pnl:
		res.append([p[0], UserCoinAccount.map[p[0]][0], p[1],p[2],UserCoinAccount.map[p[0]][1]])

	return render_template('pnl.html', pnl=res)

@app.route('/blotter')
def blotter():
	blotters= get_all_blotter()

	return render_template('blotter.html',blotter=blotters)



if __name__ == "__main__":
	app.run(debug=True)