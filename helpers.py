from functools import wraps
import requests
import os
from cs50 import SQL
from flask import session, redirect
import time
import json

db = SQL('sqlite:///database.db')

def login_required(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def convert(currency_from, currency_to):
    try:
        url = "https://alpha-vantage.p.rapidapi.com/query"
        querystring = {"to_currency":currency_to,"function":"CURRENCY_EXCHANGE_RATE","from_currency":currency_from}

        headers = {
            'x-rapidapi-host': "alpha-vantage.p.rapidapi.com",
            'x-rapidapi-key': os.getenv("API_KEY")
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
    except:
        return False


    sql_string = "SELECT id, name FROM currencies WHERE name=? or name=?"
    rows = db.execute(sql_string, currency_to, currency_from)
    if rows[0]["name"] == currency_from:
        id_from = rows[0]["id"]
        id_to = rows[1]["id"]
    else:
        id_from = rows[1]["id"]
        id_to = rows[0]["id"]
    
    json.loads(response.text)
    data = json.loads(response.text)["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
    sql_insert = "INSERT INTO conversions VALUES (?, ?, ? )"
    db.execute(sql_insert, id_from, id_to, data)
    return True


def monthly_trend(currency_from, currency_to):
    try:
        url = "https://alpha-vantage.p.rapidapi.com/query"
        querystring = {"from_symbol":currency_from,"to_symbol":currency_to,"function":"FX_MONTHLY","datatype":"json"}

        headers = {
            'x-rapidapi-host': "alpha-vantage.p.rapidapi.com",
            'x-rapidapi-key': os.getenv("API_KEY")
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        response.raise_for_status()

    except:
        return False

    sql_string = "SELECT id, name FROM currencies WHERE name=? or name=?"
    rows = db.execute(sql_string, currency_to, currency_from)
    if rows[0]["name"] == currency_from:
        id_from = rows[0]["id"]
        id_to = rows[1]["id"]
    else:
        id_from = rows[1]["id"]
        id_to = rows[0]["id"]

    json.loads(response.text)
    data = json.loads(response.text)["Time Series FX (Monthly)"]
    for i in data:
        i = date
        opn = data[i]["1. open"]
        high = data[i]["2. high"]
        low = data[i]["3. low"]
        close = data[i]["4. close"]
        sql_insert = "INSERT INTO monthly_trends(currency_from_id, currency_to_id, high, low, open, close, date) VALUES (?, ?, ?, ?, ?, ?, ?)"
        db.execute(sql_insert, id_from, id_to, high, low, opn, close,date)
 
    return True



def daily_trend(currency_from, currency_to):   
    try:
        url = "https://alpha-vantage.p.rapidapi.com/query"
        querystring = {"from_symbol":currency_from,"function":"FX_DAILY","to_symbol":currency_to,"outputsize":"compact","datatype":"json"}

        headers = {
            'x-rapidapi-host': "alpha-vantage.p.rapidapi.com",
            'x-rapidapi-key': os.getenv("API_KEY")
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
    except:
        return False

    sql_string = "SELECT id, name FROM currencies WHERE name=? or name=?"
    rows = db.execute(sql_string, currency_to, currency_from)
    if rows[0]["name"] == currency_from:
        id_from = rows[0]["id"]
        id_to = rows[1]["id"]
    else:
        id_from = rows[1]["id"]
        id_to = rows[0]["id"]

    json.loads(response.text)
    data = json.loads(response.text)["Time Series FX (Daily)"]
    for i in data:
        date = i
        opn = data[i]["1. open"]
        high = data[i]["2. high"]
        low = data[i]["3. low"]
        close = data[i]["4. close"]
        sql_insert = "INSERT INTO daily_trends(currency_from_id, currency_to_id, high, low, open, close, date) VALUES (?, ?, ?, ?, ?, ?, ?)"
        db.execute(sql_insert, id_from, id_to, high, low, opn, close, date)

    return True

def get_currency_names():
    sql_string = "SELECT name FROM currencies"
    rows = db.execute(sql_string)

    global currency_list
    currency_list = []
    for i in range(0, len(rows)):
        currency_list.append(rows[i]["name"])
    print(currency_list)

def get_daily_standings():
    k = 0                       # keep track of API calls to attain limit of 5/min , independent of loop iterators
    for i in range(0, len(currency_list)):
        for j in range(0, len(currency_list)):
            if i == j:
                continue
            if k == 5:
                k = 0
                time.sleep(100)
            daily_trend(currency_list[i], currency_list[j])
            k += 1

def get_conversions():
    k = 0                       # keep track of API calls to attain limit of 5/min , independent of loop iterators
    for i in range(0, len(currency_list)):
        for j in range(0, len(currency_list)):
            if i == j:
                continue
            if k == 5:
                k = 0
                time.sleep(100)
            convert(currency_list[i], currency_list[j])
            k += 1

def get_monthly_standings():
    k = 0                       # keep track of API calls to attain limit of 5/min , independent of loop iterators
    for i in range(0, len(currency_list)):
        for j in range(0, len(currency_list)):
            if i == j:
                continue
            if k == 5:
                k = 0
                time.sleep(100)

            monthly_trend(currency_list[i], currency_list[j])
            k += 1

def getFromApi():
    # each function accesses the API for approximately 6 minutes to get the data without exceeding limits
    # each function handles API accesses internally

   # time.sleep(15)
    get_daily_standings()
   # time.sleep(100)
    #get_conversions()
    time.sleep(100)
    get_monthly_standings()

# read api data from database
def readData(fromCur, toCur, typeOfData):
    typeOfData.lower()
    if typeOfData == "convert":
        rows = db.execute("SELECT trend FROM conversions WHERE currency_from_id=? AND currency_to_id=?", fromCur, toCur)

    elif typeOfData == "daily":
        rows = db.execute("SELECT close FROM conversions WHERE currency_from_id=? AND currency_to_id=?", fromCur, toCur)
    else:
        rows = db.execute("SELECT close FROM conversions WHERE currency_from_id=? AND currency_to_id=?", fromCur, toCur)
    
    return str(rows[0]).strip("\n")

# parse json text
def parseData(jsn):
    # data = json.loads(jsn)
    print(jsn)

if __name__ == "__main__":
    get_currency_names()
    getFromApi()