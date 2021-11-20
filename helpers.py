from functools import wraps
import requests
import os
from cs50 import SQL
from flask import session, redirect

db = SQL('sqlite:///database.db')

def login_required(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def convert(currency_from, currency_to):

    url = "https://alpha-vantage.p.rapidapi.com/query"
    querystring = {"to_currency":currency_to,"function":"CURRENCY_EXCHANGE_RATE","from_currency":currency_from}

    headers = {
        'x-rapidapi-host': "alpha-vantage.p.rapidapi.com",
        'x-rapidapi-key': os.getenv("API_KEY")
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    sql_string = "SELECT id, name FROM currencies WHERE name=? or name=?"
    rows = db.execute(sql_string, currency_to, currency_from)
    if rows[0]["name"] == currency_from:
        id_from = rows[0]["id"]
        id_to = rows[1]["id"]
    else:
        id_from = rows[1]["id"]
        id_to = rows[0]["id"]

    sql_insert = "INSERT INTO conversions VALUES (?, ?, ? )"
    db.execute(sql_insert, id_from, id_to, response.text)


def monthly_trend(currency_from, currency_to):      # relative to the KES
    url = "https://alpha-vantage.p.rapidapi.com/query"
    querystring = {"from_symbol":currency_from,"to_symbol":currency_to,"function":"FX_MONTHLY","datatype":"json"}

    headers = {
        'x-rapidapi-host': "alpha-vantage.p.rapidapi.com",
        'x-rapidapi-key': os.getenv("API_KEY")
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    sql_string = "SELECT id, name FROM currencies WHERE name=? or name=?"
    rows = db.execute(sql_string, currency_to, currency_from)
    if rows[0]["name"] == currency_from:
        id_from = rows[0]["id"]
        id_to = rows[1]["id"]
    else:
        id_from = rows[1]["id"]
        id_to = rows[0]["id"]

    sql_insert = "INSERT INTO monthly_trends VALUES (?, ?, ? )"
    print(response.text)
    db.execute(sql_insert, id_from, id_to, response.text)



def daily_trend(currency_from, currency_to):      # relative to the KES
    url = "https://alpha-vantage.p.rapidapi.com/query"
    querystring = {"from_symbol":currency_from,"function":"FX_DAILY","to_symbol":currency_to,"outputsize":"compact","datatype":"json"}

    headers = {
        'x-rapidapi-host': "alpha-vantage.p.rapidapi.com",
        'x-rapidapi-key': os.getenv("API_KEY")
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    sql_string = "SELECT id, name FROM currencies WHERE name=? or name=?"
    rows = db.execute(sql_string, currency_to, currency_from)
    if rows[0]["name"] == currency_from:
        id_from = rows[0]["id"]
        id_to = rows[1]["id"]
    else:
        id_from = rows[1]["id"]
        id_to = rows[0]["id"]

    sql_insert = "INSERT INTO daily_trends VALUES (?, ?, ? )"
    print(response.text)
    db.execute(sql_insert, id_from, id_to, response.text)

def get_currency_names():
    sql_string = "SELECT name FROM currencies"
    rows = db.execute(sql_string)

    global currency_list
    currency_list = []
    for i in range(0, len(rows)):
        currency_list.append(rows[i]["name"])
    print(currency_list)

def get_daily_standings():
    for i in range(0, len(currency_list)):
        for j in range(0, len(currency_list)):
            if i == j:
                continue
            daily_trend(currency_list[i], currency_list[j])

def get_conversions():
    for i in range(0, len(currency_list)):
        for j in range(0, len(currency_list)):
            if i == j:
                continue
            convert(currency_list[i], currency_list[j])

def get_monthly_standings():
    for i in range(0, len(currency_list)):
        for j in range(0, len(currency_list)):
            if i == j:
                continue
            monthly_trend(currency_list[i], currency_list[j])


get_currency_names()
get_conversions()
get_daily_standings()
get_monthly_standings()