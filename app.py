from flask import Flask, jsonify, request
from flask.helpers import send_file
import requests
import finnhub
from pymongo import MongoClient
from datetime import datetime, timedelta
import os



finnhub_client = finnhub.Client(api_key="cvpapapr01qve7inpjp0cvpapapr01qve7inpjpg")

def load_symbols_file():
    try:
        with open("symbols.txt", "r") as file:
            symbols_data = file.read()
            print("File loaded successfully at startup:")
            return symbols_data.split("\n")
    except FileNotFoundError:
        print("symbols.txt file not found.")
        return ""
    
def get_mongo_client():
    try:

        client = MongoClient("connection_string")
        print("Connected to MongoDB successfully!")
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

# Call the function to load the file at startup
symbols = load_symbols_file()

def loadAllCongressTrades():
    for symbol in symbols:
        url = "https://finnhub.io/api/v1/stock/congressional-trading?symbol="+symbol+"&token=cvpapapr01qve7inpjp0cvpapapr01qve7inpjpg"

        # Send the GET request
        response = requests.get(url)
        responseData = response.json()

        print(f"Loading congress trades for {symbol}")
        all_dates = set()
        if "data" in responseData and responseData["data"]:
            all_dates.update(trade["transactionDate"] for trade in responseData["data"] if "transactionDate" in trade)
        
        if "results[]" not in response.text:
            with open("congressional_trades.txt", "a") as file:
                file.write(response.text)
                print("File loaded successfully appended: Trades")
                #loadAllTicks(all_dates, symbol)

        
    
def loadAllTicks(all_dates,symbol):    
    for date in all_dates:
        print(f"Loading ticks for {symbol} on {date}")
        saveTicks(symbol,getNextDate(date,30))
        saveTicks(symbol,getNextDate(date,60))
        saveTicks(symbol,getNextDate(date,90))
        saveTicks(symbol,getNextDate(date,120))

def saveTicks(symbol, date):
    url = "https://api.polygon.io/v3/quotes/"+symbol+"?timestamp="+date+"&order=asc&limit=1&sort=timestamp&apiKey=p4qiD7nLAIpvJqOjr6CPyelijxzfNy4X"
        
    response = requests.get(url)
    if "results[]" not in response.text:
        responseData = response.json()
        results = response.text.replace("results", symbol)
        with open("congressional_ticks.txt", "a") as file:
            file.write(results.__str__())
            print("File loaded successfully appended: Ticks")

def getNextDate(date,change):
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    new_date_obj = date_obj + timedelta(days=change)
    return new_date_obj.strftime('%Y-%m-%d')

#def save_to_mongo(data,db_name, collection_name):
#    if mongo_client:
#        try:
#            db = mongo_client[db_name]  # Replace with your database name
#            print(f"Connected to db: {db_name}")
#            collection = db[collection_name]
#            print(f"Connected to collection: {collection_name}")
#            collection.insert_many(data)
#            print(f"Inserted {len(data)} records into {collection_name} collection.")
#
#            return {"message": "Data saved to MongoDB successfully!"}
#        except Exception as e:
#            return {"error": str(e)}
#    else:
#        return {"error": "MongoDB connection not established."}
    
#loadAllCongressTrades()

app = Flask(__name__)

@app.route("/")
def initialPage():
    return send_file("templates/index.html")

@app.route("/index")
def indexPage():
    return send_file("templates/index.html")

@app.route("/result",methods=['POST'])
def resultPage():
    return send_file("templates/result.html")

@app.route("/recommendation",methods=['POST'])
def recommendationPage():
    return send_file("templates/recommendation.html")
