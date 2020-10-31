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
from classes.stock import Stock
from classes.screener import Screener

name_testdict = "SQ"

# Relevant API calls
""" 
Historical data
"""
# Hist. (daily) prices
# https://financialmodelingprep.com/api/v3/historical-price-full/AAPL?from=2018-03-12&to=2019-03-12&apikey=e525189853e67230f6ff8f8734c00b5b
# Hist. dividends:
# https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/AAPL?apikey=e525189853e67230f6ff8f8734c00b5b
""" 
Stock Screener
"""
# Search companies by several attributes (marketCap, industry, sector etc.) example:
# https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan=1000000000&betaMoreThan=1&volumeMoreThan=10000&sector=Technology&industry=Software&exchange=NASDAQ&dividendMoreThan=0&limit=100&apikey=e525189853e67230f6ff8f8734c00b5b

"""
Analyst Estimates (Paid feature =( )
"""
# Earnings, Revenue etc. for the next few years
# https://financialmodelingprep.com/api/v3/analyst-estimates/AAPL?period=quarter&limit=30&apikey=e525189853e67230f6ff8f8734c00b5b
# https://financialmodelingprep.com/api/v3/analyst-estimates/AAPL?limit=30&apikey=e525189853e67230f6ff8f8734c00b5b
""" 
Calendars
"""
# IPOs (Paid feature =( ) , Dividends etc.


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

Square = Stock('SQ')
#PayPal = Stock('PYPL')
#CDProjekt = Stock('7CD')
#Visa = Stock('V')
#Mastercard = Stock('MA')
#Microsoft = Stock('MSFT')


# Read data from file if it exists:
#if Path("data/"+name_testdict+".json").is_file():
#    with open("data/"+name_testdict+".json") as file:
#        company_dict = json.load(file)
#else:
#    company_dict = f.build_dict(name_testdict)
#    with open("data/"+name_testdict+".json",'w') as file:
#        # Serialize data into file:
#        json.dump(company_dict, file)

#f.chart(company_dict["income_statement"], type="revenue")

#f.chart(Square.fundamentals["income_statement"], type="revenue")
#f.chart(PayPal.fundamentals["income_statement"], type="revenue")
#f.chart(Visa.fundamentals["income_statement"], type="revenue")
#f.chart(Mastercard.fundamentals["income_statement"], type="revenue")

#Screener.plot_revenue([Square, PayPal])
#Screener.plot_revenue(Square)
#Screener.plot_netprofit(Square)
#Screener.plot_revenue(CDProjekt)

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