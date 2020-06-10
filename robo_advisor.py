#
# INFO INPUTS
#

import requests
import json # included in python language already

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo"
response = requests.get(request_url)
# print(type(response)) #> class 'requests.models.Response'
# print(response.status_code) #> 200 (count)
# print(response.text) #> str (so need JSON module to process into dictionary)

parsed_response = json.loads(response.text)

breakpoint()






#
# INFO OUTPUTS
#