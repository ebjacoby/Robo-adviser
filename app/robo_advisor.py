#
# INFO INPUTS
#
import csv
import json # included in python language already
import os

from dotenv import load_dotenv
from statistics import mean
import requests
import datetime

load_dotenv() #loads contents of the .env file into the script's environment

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

def to_percent(number):
    return "{:.2%}".format(number)


api_key = os.environ.get("ALPHA_VANTAGE_API") #> "demo"


#symbol = input("Please input a stock identifier: ") # TODO accept user input

try:
    symbol = input("Please input a stock identifier: ")
    symbol_length = len(symbol)
    if (symbol_length < 3 or symbol_length > 5) or not symbol.isalpha():
        print("The system is expecting a properly-formed stock symbol like 'MSFT' or 'IBM' - please try again!")
        exit()

    #request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}"
    #request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={api_key}"
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={api_key}"
    response = requests.get(request_url)

    # print(type(response)) #> class 'requests.models.Response'
    # print(response.status_code) #> 200 (count)
    # print(response.text) #> str (so need JSON module to process into dictionary)

    parsed_response = json.loads(response.text)

    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

except Exception:
    print("The system is expecting a properly-formed stock symbol like 'MSFT' or 'IBM' - please try again!")
    exit()

#breakpoint()

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys()) # TODO: assumes first day is on top, but consider sort to ensure latest day is first

latest_day = dates[0] #each date is a str

latest_close = tsd[latest_day]["4. close"]
latest_volume = tsd[latest_day]["5. volume"]

# maximum and minimum of all the high prices
high_prices = []
low_prices = []
closing_prices = []
volumes = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))
    closing_price = tsd[date]["4. close"]
    closing_prices.append(float(closing_price))
    volume = tsd[date]["5. volume"]
    volumes.append(float(volume))

recent_high = max(high_prices[:100]) #[:100] = most recent 100 days
recent_low = min(low_prices[:100])

recent_average_closing_price = mean(closing_prices[:100])
recent_average_volume = mean(volumes[:100])

fiftytwo_week_high = max(high_prices[:365])
fiftytwo_week_low = min(low_prices[:365])

csv_file_name = symbol + "_prices.csv"
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", csv_file_name)

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
with open(csv_file_path, "w", newline='') as csv_file: # "w" means "open the file for writing"
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
    
    x = 0
    closing_prices_TSR = []

    for x in range(100):
        closing_price_percent = (float(closing_prices[x]) / float(closing_prices[x+1])) - 1
        # closing_price_percent = closing_price_percent
        closing_prices_TSR.append(closing_price_percent)
    
    y = 0
    cdfs = []

    for y in range(100):
        cdf = 1 + y #cumulative_distribution_function
        cdf2 = cdf / 100
        cdfs.append(cdf2)
    
    percent_change_cdf = {}
    closing_prices_TSR.sort()

    for i in range(100):
        percent_change_cdf[cdfs[i]] = closing_prices_TSR[i]

    sum_gains = sum(closing_prices_TSR)

    percentage = -1 
    for percent, gain in sorted(percent_change_cdf.items(),key=lambda each:each[1]):
        if gain > 0:
            percentage = percent
            break
    if percentage == -1:
        print("don't buy")
    else:
        print("-------------------------")

#time
current_day = datetime.date.today()
now = datetime.datetime.now()
current_time = now.strftime("%H:%M:%S")
full_time = str(current_day) + " " + str(current_time)

# app/robo_advisor.py

print("-------------------------")
print("SELECTED SYMBOL: ", symbol) #MICROSOFT KEY
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: ", full_time) #DATETIME MODULE
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")#format string
print(f"LATEST CLOSE: {to_usd(float(latest_close))}") #string version of a float?
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print(f"LATEST VOLUME TRADED: {(float(latest_volume))}")
print(" ")
print(f"52-WEEK HIGH: {to_usd(float(fiftytwo_week_high))}")
print(f"52-WEEK LOW: {to_usd(float(fiftytwo_week_low))}")
print(" ")
print(f"100-DAY AVERAGE CLOSING PRICE: {to_usd(float(recent_average_closing_price))}")
print(f"100-DAY AVARAGE TRADING VOLUME: {(float(recent_average_volume))}")
print("-------------------------")

if sum_gains > 0:
    print("BUY")
    print("-------------------------")
    print("RECOMMENDATION: BUY THIS STOCK! ACCORDING TO OUR TIME-SERIES ANALYSIS,") 
    print("USING A CUMULATIVE DISTRIBUTION FUNCTION TO ESTIMATE RETURNS,")
    print("WE PROJECT THAT THERE IS A ", to_percent(1 - percentage), " CHANCE THAT YOU WILL EARN") 
    print("A GAIN OF ", to_percent(percent_change_cdf[percentage]), " OR GREATER.")
    print("-------------------------")
    print("YOUR RETURN IS PROJECTED TO BE", to_percent(sum_gains), "IF YOU PURCHASE THIS STOCK!")
else:
    print("DO NOT BUY")
    print("-------------------------")
    print("RECOMMENDATION: DO NOT BUY THIS STOCK! ACCORDING TO OUR TIME-SERIES ANALYSIS,")
    print("USING A CUMULATIVE DISTRIBUTION FUNCTION TO ESTIMATE RETURNS,")
    print("WE PROJECT YOUR RETURN TO BE", to_percent(percentage), " CHANCE THAT YOU WILL INCUR")
    print("A LOSS OF ", to_percent(percent_change_cdf[percentage]) * -1, " OR GREATER.")
    print("-------------------------")
    print("YOUR RETURN IS PROJECTED TO BE", to_percent(sum_gains), "IF YOU PURCHASE THIS STOCK.")

print("-------------------------")
print(f"WRITING DATA TO CSV: data\{csv_file_name}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")



#
# INFO OUTPUTS
#

# check notes on csv module and os module (helps with file location)
# csv_file_path = "data/MSFT_prices.csv" # a relative filepath

