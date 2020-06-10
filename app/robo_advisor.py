#
# INFO INPUTS
#
import csv
import json # included in python language already
import os

from dotenv import load_dotenv
import requests

load_dotenv() #loads contents of the .env file into the script's environment

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

api_key = os.environ.get("ALPHAVANTAGE_API_KEY") #> "demo"

symbol = "MSFT" # TODO accept user input

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}"

response = requests.get(request_url)

# print(type(response)) #> class 'requests.models.Response'
# print(response.status_code) #> 200 (count)
# print(response.text) #> str (so need JSON module to process into dictionary)

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

#breakpoint()

tsd = parsed_response["Time Series (5min)"]

dates = list(tsd.keys()) # TODO: assumes first day is on top, but consider sort to ensure latest day is first

latest_day = dates[0] #each date is a str

latest_close = tsd[latest_day]["4. close"]

# maximum and minimum of all the high prices
high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "MSFT_prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    
    #looping
    #writer.writerow({"timestamp": "TODO", "open": "TODO", "high": "TODO", "low": "TODO", "close": "TODO", "volume": "TODO",})
    #assembling a dictionary that will get into the csv file (with examples)
    
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })


# app/robo_advisor.py

print("-------------------------")
print("SELECTED SYMBOL: XYZ") #MICROSOFT KEY
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm") #DATETIME MODULE
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")#format string
print(f"LATEST CLOSE: {to_usd(float(latest_close))}") #string version of a float?
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO") #HAVE TO DO ON MY OWN>>>>>>>>>
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")



#
# INFO OUTPUTS
#

# check notes on csv module and os module (helps with file location)
# csv_file_path = "data/MSFT_prices.csv" # a relative filepath

