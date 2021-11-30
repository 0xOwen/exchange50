from flask import jsonify
from cs50 import SQL

db = SQL('sqlite:///database.db')


def fetch_monthly(from_currency, to_currency):
    query = "SELECT open , close, date FROM monthly_trends WHERE currency_from_id=? AND currency_to_id=? ORDER BY date DESC LIMIT 12"
    data = db.execute(query, from_currency, to_currency)
    data[0]["from_name"] = get_name(from_currency)
    data[0]["to_name"] = get_name(to_currency)
    return data

def fetch_daily(from_currency, to_currency):
    query = "SELECT high, low, open , close, date FROM daily_trends WHERE currency_from_id=? AND currency_to_id=? ORDER BY date DESC LIMIT 25"
    data = db.execute(query, from_currency, to_currency)
    data[0]["from_name"] = get_name(from_currency)
    data[0]["to_name"] = get_name(to_currency)
    return data

def get_conversion(from_currency, to_currency):
    query = "SELECT trend from conversions WHERE currency_from_id=? AND currency_to_id=?"
    data = db.execute(query, from_currency, to_currency)
    data[0]["from_name"] = get_name(from_currency)
    data[0]["to_name"] = get_name(to_currency)
    return data

def get_name(currency):
    query = "SELECT description FROM currencies WHERE id=?"
    name = db.execute(query, currency)
    return name[0]["description"]


    


