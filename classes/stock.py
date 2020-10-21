from financeAPI.financeAPI_lib import FinanceAPI as fapi
from pathlib import Path
import json

class Stock:

    n_stocks = 0
    API = fapi()

    def __init__(self, symbol:str):
        self.symbol = symbol
        self.fundamentals = self._initData()
        Stock.n_stocks += 1

    @classmethod
    def counter(cls):
        return cls.n_stocks

    def _initData(self, save=False):
        fundamentals = {}
        if (Stock.API.key_registered == False):
            # Check for API Key and load
            if Path("financeAPI/Secret_Key.txt").is_file():
                with open('financeAPI/Secret_Key.txt') as file:
                    key = file.read()
                Stock.API.registerKey_(key)
            else:
                print("No file with API key found")
                exit()

        profile = Stock.API.callAPI_financialModelingPrep_(self.symbol, call="profile")
        # self.metrics_data_(self.symbol)
        # self.ratios_data_(self.symbol)

        fundamentals['symbol'] = self.symbol

        """
        profile data
        """
        fundamentals["profile"] = {}
        d_profile = {}
        for k in profile.keys():
            d_profile[k] = profile[k]
            fundamentals["profile"] = d_profile

        # """
        # metrics data
        # """
        # for k in self.metrics['metrics'][0].keys():
        #     data_dict[k]=self.metrics['metrics'][0][k]
        #
        # """
        # ratios data
        # """
        # c=[(k,v) for k,v in self.ratios[0].items()]
        # for k in c[2:]:
        #     data_dict[k[0]]=k[1]

        """
        income statement data
        """
        fundamentals["income_statement"] = {}
        #Annual
        income_statement = Stock.API.callAPI_financialModelingPrep_(self.symbol, call="income_statement")
        # for year in d_income_statement.keys():
        for e in range(0, len(income_statement)):
            d_incomeStatement = {}
            for k in income_statement[e].keys():
                d_incomeStatement[k] = income_statement[e][k]
            # just use year for indexing the single statements -> [0:4]
            if income_statement[e]["date"][0:4] not in fundamentals["income_statement"]:
                fundamentals["income_statement"][income_statement[e]["date"][0:4]] = {}
            fundamentals["income_statement"][income_statement[e]["date"][0:4]]["Annual"] = d_incomeStatement

        # Quarters
        income_statement_quarter = Stock.API.callAPI_financialModelingPrep_(self.symbol, period="quarter", call="income_statement")
        for e in range(0, len(income_statement_quarter)):
            d_incomeStatement = {}
            for k in income_statement_quarter[e].keys():
                d_incomeStatement[k] = income_statement_quarter[e][k]
            # just use year for indexing the single statements -> [0:4]
            if income_statement_quarter[e]["date"][0:4] not in fundamentals["income_statement"]:
                fundamentals["income_statement"][income_statement_quarter[e]["date"][0:4]] = {}
            fundamentals["income_statement"][income_statement_quarter[e]["date"][0:4]][income_statement_quarter[e]["period"]] = d_incomeStatement


        # save dictionary to data-folder
        if save:
            with open("data/" + self.symbol + ".json", 'w') as file:
                # Serialize data into file:
                json.dump(fundamentals, file)

        return fundamentals

    def build_dict(self, symbol, save=False):
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
        # for year in d_income_statement.keys():
        for e in range(0, len(d_income_statement)):
            dict_incomeStatement = {}
            for k in d_income_statement[e].keys():
                dict_incomeStatement[k] = d_income_statement[e][k]
            # just use year for indexing the single statements -> [0:4]
            data_dict["income_statement"][d_income_statement[e]["date"][0:4]] = dict_incomeStatement

        # save dictionary to data-folder
        if save:
            with open("data/" + symbol + ".json", 'w') as file:
                # Serialize data into file:
                json.dump(data_dict, file)
        return data_dict
