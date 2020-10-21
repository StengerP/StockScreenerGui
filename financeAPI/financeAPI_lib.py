"""
A finance API class using the API from https://financialmodelingprep.com/
NOTE: You need to register on their website to obtain your own secret API key
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import plotly.graph_objects as go
from urllib.request import urlopen
from pathlib import Path

class FinanceAPI():
    """
    Core class
    """
    
    def __init__(self):
        """
        Initiates the object
        """
        self.key = ''
        self.key_registered = False
        self.originUrl = "https://financialmodelingprep.com/api/v3/"
        pass
    
    def registerKey_(self,key):
        """
        Registers a secret API key to the object
        """
        assert type(key) is str,"Key must be a string"
        self.key = str(key)
        self.key_registered = True
    
    def __repr__(self):
        return ("This is a finance API class.\n")

        
    def metrics_data_(self,symbol):
        """
        Pulls the metrics data from the API for the given ticker symbol

        Parameters
        ----------
        symbol : A ticker symbol (str) e.g. 'MSFT','FB','AAPL', or 'TWTR'

        Returns
        -------
        None. Updates the self.metrics with the data. 
        """
        if not self.key_registered:
            print("API key not registered yet.")
            return None
        
        url = "https://financialmodelingprep.com/api/v3/"+\
            "company-key-metrics/"+str(symbol)+'?apikey='+self.key
        response = urlopen(url)
        data = response.read().decode("utf-8")
        self.metrics = json.loads(data)
        
    def ratios_data_(self,symbol):
        """
        Pulls the ratios data from the API for the given ticker symbol

        Parameters
        ----------
        symbol : A ticker symbol (str) e.g. 'MSFT','FB','AAPL', or 'TWTR'

        Returns
        -------
        None. Updates the self.ratios with the data. 
        """
        if not self.key_registered:
            print("API key not registered yet.")
            return None
        
        url = "https://financialmodelingprep.com/api/v3/"+\
            "ratios/"+str(symbol)+'?apikey='+self.key
        response = urlopen(url)
        data = response.read().decode("utf-8")
        self.ratios = json.loads(data)

    
    def build_dict(self,symbol,save=False):
        """
        Builds a dictionary with a given ticker symbols
        
        Parameters
        ----------
        symbol : A ticker symbol (str) e.g. 'MSFT','FB','AAPL', or 'TWTR'

        Returns
        -------
        A dictionary with all the profile and metrics data pulled from the API
        """
        # Pull data
        if not self.key_registered:
            print("API key not registered yet.")
            return None

        d_profile = self.callAPI_financialModelingPrep_(symbol, call="profile")
        d_income_statement = self.callAPI_financialModelingPrep_(symbol, call="income_statement")
        # self.metrics_data_(symbol)
        # self.ratios_data_(symbol)

        data_dict = {}
        data_dict['symbol'] = symbol

        # Profile data
        data_dict["profile"] = {}
        dict_profile = {}
        for k in d_profile.keys():
            dict_profile[k] = d_profile[k]
        data_dict["profile"] = dict_profile

        # # Metrics data
        # for k in self.metrics['metrics'][0].keys():
        #     data_dict[k]=self.metrics['metrics'][0][k]
        # # Ratios data
        # c=[(k,v) for k,v in self.ratios[0].items()]
        # for k in c[2:]:
        #     data_dict[k[0]]=k[1]

        # income statement data
        data_dict["income_statement"] = {}
        #for year in d_income_statement.keys():
        for e in range(0, len(d_income_statement)):
            dict_incomeStatement = {}
            for k in d_income_statement[e].keys():
                dict_incomeStatement[k] = d_income_statement[e][k]
            # just use year for indexing the single statements -> [0:4]
            data_dict["income_statement"][d_income_statement[e]["date"][0:4]] = dict_incomeStatement

        #save dictionary to data-folder
        if save:
            with open("data/" + symbol + ".json", 'w') as file:
                # Serialize data into file:
                json.dump(data_dict, file)
        return data_dict


    def available_data(self,data_type='profile'):
        """
        Prints a list of data items that are available
        
        Arguments
        ----------
        data_type: One of 'profile','metrics',or 'ratios'
        
        Returns
        --------
        None. Prints a list.
        """
        assert str(data_type) in ['profile','metrics','ratios'], \
        "Data type not recognized. Should be one of \'profile\',\'metrics\',or \'ratios\'"
        
        available_data = []
        if data_type=='profile':    
            for k in self.profile['profile'].keys():
                if self.profile['profile'][k] is not None:
                    available_data.append(k)
            print("Following data are available for profile")
            print("="*60)
            for d in available_data[:-1]:
                print(d,end=', ')
            print(available_data[-1],end='.')
        
        if data_type=='metrics':    
            for k in self.metrics['metrics'][0].keys():
                if self.metrics['metrics'][0][k] is not None:
                    available_data.append(k)
            print("Following data are available for metrics")
            print("="*60)
            for d in available_data[:-1]:
                print(d,end=', ')
            print(available_data[-1],end='.')
            
        if data_type=='ratios':    
            c=[(k,v) for k,v in self.ratios[0].items()]
            for k in c[2:]:
                if k[1] is not None:
                    available_data.append(k[0])
            print("Following data are available for ratios")
            print("="*60)
            for d in available_data[:-1]:
                print(d,end=', ')
            print(available_data[-1],end='.')
    
    def cols_numeric_(self):
        """
        Transforms columns to numeric (float) wherever applicable
        """
        for c in self.df.columns:
            try:
                self.df[c] = self.df[c].apply(float)
            except ValueError:
                pass
    
    def replace_None_(self):
        """
        Replaces NoneType data by np.nan in the DataFrame
        """
        self.df.fillna(value=pd.np.nan, inplace=True)
    
    def build_dataframe(self,lst):
        """
        Builds a DataFrame with a given list of ticker symbols
        
        Parameters
        ----------
        lst : A list of ticker symbols (str) 
            e.g. ['MSFT','FB','AAPL','TWTR']

        Returns
        -------
        A Pandas DataFrame with all the data pulled from the API, 
        indexed by the symbol (company)
        """
        if not self.key_registered:
            print("API key not registered yet.")
            return None
        
        data_companies = []
        for c in lst:
            data_companies.append(self.build_dict(c, save=True))
        # Build the DataFrame
        self.df = pd.DataFrame(data_companies)
        # Convert to numeric columns wherever applicable
        self.replace_None_()
        self.cols_numeric_()
        
        return self.df
    
    def bar_chart(self,var='price',**kwargs):
        """
        Plots a bar chart of the given variable
        
        Parameters
        ----------
        var : Name of the variable to be plotted (str)
            e.g. 'price', 'PE ratio', 'Book Value per Share'

        Returns
        -------
        None
        """
        plt.figure(figsize=(10,4))
        plt.title("{}".format(var),fontsize=18)
        plt.bar(x=self.df['companyName'],height=self.df[var],**kwargs)
        plt.xticks(fontsize=14,rotation=45)
        plt.yticks(fontsize=14)
        plt.ylabel(var,fontsize=16)
        plt.show()

    def scatter(self,varX,varY,sizeZ=None,**kwargs):
        """
        Plots a scatter chart of the given variable pair,
        and (optionally) size the as per a third variable
        
        Parameters
        ----------
        varX : Name of the x-axis variable (str), e.g. 'price', 'PE ratio', 'Book Value per Share'
        varY : Name of the x-axis variable (str), e.g. 'price', 'PE ratio', 'Book Value per Share'
        sizeZ : Name of the variable (str) for sizing, e.g. 'price', 'PE ratio', 'Book Value per Share'

        Returns
        -------
        None
        """
        if sizeZ is not None:
            scale = 1000/(self.df[sizeZ].max()**2)
        plt.figure(figsize=(10,4))
        plt.title("{} vs. {}".format(varX,varY),fontsize=18)
        if sizeZ is not None:
            plt.scatter(x=self.df[varX],y=self.df[varY],s=scale*self.df[sizeZ]**2,**kwargs)
        else:
            plt.scatter(x=self.df[varX],y=self.df[varY],s=200,**kwargs)
        for i in (range(len(self.df))):
            plt.annotate(s=self.df['symbol'][i],
                         xy=(self.df[varX][i],
                             self.df[varY][i]))
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.xlabel(varX,fontsize=16)
        plt.ylabel(varY,fontsize=16)
        plt.show()

    def chart(self, input,type, **kwargs):
        """
        Plots a bar chart of the given input[type]

        Parameters
        ----------
        var : Name of the variable to be plotted (str)
            e.g. 'price', 'PE ratio', 'Book Value per Share'

        Returns
        -------
        None
        """
        data_x = []
        data_y = []
        for k in input.keys():
            data_x.append(k)
            data_y.append(input[k][type])
        #growth = (data_y[1] - data_y[0])/data_y[1]
        fig = go.Figure(data=[go.Bar(x=data_x,y=data_y)]) #hovertext=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19'])])
        # Customize aspect
        fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                          marker_line_width=1.5, opacity=0.6)
        fig.update_layout(title_text='Historical '+type, yaxis=dict(title="Revenue in Billion USD"), xaxis=dict(title="year"))
        fig.show()

    def start_stock_screener(self):
        parameters = self.select_filter()

        results = self.callAPI_financialModelingPrep_(parameters, "stock_screener") #("AAPL", "profile")

        for e in range(0, len(results)):
            print(results[e]["symbol"])


    def select_filter(self):
        """
        set filter Parameters for the stock screener search

        Parameters
        ----------
        available Parameters:   marketCapMoreThan & marketCapLowerThan : number  (zB. marketCapMoreThan=1000000)
                                betaMoreThan & betaLowerThan           : number
                                volumeMoreThan & volumeLowerThan       : number
                                dividendMoreThan & dividendLowerThan   : number
                                sector : Consumer Cyclical - Energy - Technology - Industrials - Financial Services
                                         Basic Materials - Communication Services - Consumer Defensive - Healthcare
                                         Real Estate - Utilities - Industrial Goods - Financial - Services - Conglomerates
                                exchange : nyse - nasdaq - amex - euronex - tsx - etf - mutual_fund
                                limit : number (limit of results)

        example : https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan=1000000000&volumeMoreThan=10000&sector=Technology&exchange=NASDAQ&dividendMoreThan=0&limit=100&apikey=key

        Returns
        -------
        dict with filter Parameters
        """
        # TODO place read of a GUI here later where Parameters can be selected.
        # for now static parameters:
        parameters = {"marketCapMoreThan": 100000000000, "sector": "Healthcare", "limit": 10}

        return parameters

    def callAPI_financialModelingPrep_(self, input_data, period="annual", call="profile"):
        """
        make call of the financialModelingPrep API with given parameters

        Parameters
        ----------
        input_data : dict with parameters for the call (see https://financialmodelingprep.com/developer/docs/#Stock-Screener)
                     string with Ticker Symbol of the stock
        call : specify the type of API call for constructing the string

        Returns
        -------
        results as a dictionary
        """
        if not self.key_registered:
            print("API key not registered yet.")
            return None

        if call is 'stock_screener':
            # TODO : data auf dict prüfen bzw richtige Eingabeparameter
            parameters = ""
            for k in input_data.keys():
                parameters = parameters+k+"="+str(input_data[k])+"&"
            url = self.originUrl + "stock-screener?" + parameters + 'apikey=' + self.key
            response = urlopen(url)
            return json.loads(response.read().decode("utf-8"))

        elif call is "income_statement":
            #dict_t = self.dataExisting(input_data)
            #if "income_statement" in dict_t:
            #    return dict_t["income_statement"]
            #else:
            #    url = self.originUrl + "income-statement/" + str(input_data) + "?apikey=" + self.key
            #    response = urlopen(url)
            #    return json.loads(response.read().decode("utf-8"))
            if period == "quarter":
                url = self.originUrl + "income-statement/" + str(input_data) + "?" + "period=" + str(period) + "&apikey=" + self.key
                response = urlopen(url)
            else:
                url = self.originUrl + "income-statement/" + str(input_data) + "?apikey=" + self.key
                response = urlopen(url)
            return json.loads(response.read().decode("utf-8"))
        elif call is "profile":
            dict_t = self.dataExisting(input_data)
            if "profile" in dict_t:
                return dict_t["profile"]
            else:
                url = self.originUrl + "company/profile/" + str(input_data) + '?apikey=' + self.key
                response = urlopen(url)
                data = json.loads(response.read().decode("utf-8"))
                return data["profile"]
        else:
            print("Type of API call not supported: "+call)
            return {}

        # TODO support other types of API calls in this function
        # if call is "metrics":
        # if call is "ratios":

    def dataExisting(self, symbol):
        """
        Check if dict of stock already saved in data-folder

        Parameter
        ---------
        symbol : ticker symbol of stock

        Return
        ------
        dictionary of stock or empty dictionary if file not found
        """
        # Read data from file if it exists:
        if Path("data/" + symbol + ".json").is_file():
            with open("data/" + symbol + ".json") as file:
                return json.load(file)
        else:
            return {}
