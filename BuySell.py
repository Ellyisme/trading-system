from flask_wtf import Form
from wtforms import SelectField, SubmitField, IntegerField


class BuySellForm(Form):
    transaction = SelectField('Transactions', choices=[(1, 'Buy'), (2, 'Sell')])
    coins = SelectField('Coins', choices=[(1, 'BTC'), (2, 'ETH'), (3, 'LTC')])
    quantity = IntegerField('Quantity')
    submit = SubmitField('Submit')
