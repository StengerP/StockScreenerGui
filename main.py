# Main script
from financeAPI.financeAPI_lib import FinanceAPI
# Other libraries
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import plotly.express as px
from urllib.request import urlopen

name_testdict = "SQ"


f = FinanceAPI()
print(f)

# Check for API Key and load
if Path("financeAPI/Secret_Key.txt").is_file():
    with open('financeAPI/Secret_Key.txt') as file:
        key = file.read()
    f.registerKey_(key)
else:
    print("No file with API key found")
    exit()

#f.start_stock_screener()

# Read data from file if it exists:
if Path("data/"+name_testdict+".json").is_file():
    with open("data/"+name_testdict+".json") as file:
        company_dict = json.load(file)
else:
    company_dict = f.build_dict(name_testdict)
    with open("data/"+name_testdict+".json",'w') as file:
        # Serialize data into file:
        json.dump(company_dict, file)

f.chart(company_dict["income_statement"], type="revenue")

#apple_dict=f.build_dict('AAPL')

#
# for k,v in apple_dict.items():
#     print("{}: {}".format(k,v))
#
# df = f.build_dataframe(['FB','MSFT','AAPL',"AMZN","NFLX", "GOOG"])
#
# f.available_data('profile')
#
# f.available_data('metrics')
#
# f.available_data('ratios')
#
# f.bar_chart('Book Value per Share',color='orange',edgecolor='k')
#
# f.bar_chart('debtEquityRatio')
#
# f.scatter('quickRatio','Book Value per Share',color='blue')
#
# f.scatter(varX='debtEquityRatio',
#           varY='Enterprise Value over EBITDA',
#          sizeZ='price',
#          color='red',alpha=0.6)
#
# # Only companies with market cap > 200 billion USD
# df = f.df
# df_large_cap = df[df['Market Cap']>200e9]
# df_large_cap[['companyName','Market Cap']]
#
#
# # A fresh class declration
# f2 = FinanceAPI()
# # Assigning the custom DataFrame to the `df` attribute of this new class object
# # Note we did not need to request data from the API again.
# f2.df = df_large_cap
#
# f2.bar_chart('Enterprise Value over EBITDA',color='red',edgecolor='k')