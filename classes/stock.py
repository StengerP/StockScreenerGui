from financeAPI.financeAPI_lib import FinanceAPI as fapi
from pathlib import Path
import json
import pandas as pd

class Stock:

    n_stocks = 0
    API = fapi()

    def __init__(self, symbol:str):
        self.symbol = symbol
        self.revenueAnnual = pd.DataFrame(columns=['year', 'revenue'])
        self.revenueQuarter = pd.DataFrame(columns=['quarter', 'revenue'])
        self.fundamentals = self._init_fundamentals()
        self.chart = self._load_chartHistory()
        Stock.n_stocks += 1

    @classmethod
    def counter(cls):
        return cls.n_stocks

    def _load_chartHistory(self):
        pass

    def _init_fundamentals(self, save=False):

        fundamentals = {}

        if Stock.API.key_registered == False:
            # Check for API Key and load
            if Path("financeAPI/Secret_Key.txt").is_file():
                with open('financeAPI/Secret_Key.txt') as file:
                    key = file.read()
                Stock.API.registerKey_(key)
            else:
                print("No file with API key found")
                exit()

        fundamentals['symbol'] = self.symbol
        # self.metrics_data_(self.symbol)
        # self.ratios_data_(self.symbol)

        """
        profile data
        """
        profile = Stock.API.callAPI_financialModelingPrep_(self.symbol, call="profile")
        fundamentals["profile"] = {}
        d_profile = {}
        for k in profile.keys():
            d_profile[k] = profile[k]
            fundamentals["profile"] = d_profile

        """
        income statement data
        """
        fundamentals["income_statement"] = {}

        # Annual
        income_statement = Stock.API.callAPI_financialModelingPrep_(self.symbol, call="income_statement")
        for e in range(0, len(income_statement)):
            d_incomeStatement = {}
            for k in income_statement[e].keys():
                d_incomeStatement[k] = income_statement[e][k]

            # Add to revenueAnnual
            year = income_statement[e]["date"][0:4]
            rev = income_statement[e]['revenue']
            self.revenueAnnual.loc[e] = [year, rev]

            # just use year for indexing -> [0:4]
            if year not in fundamentals["income_statement"]:
                fundamentals["income_statement"][year] = {}
            fundamentals["income_statement"][year]["Annual"] = d_incomeStatement

        # Quarters
        income_statement_quarter = Stock.API.callAPI_financialModelingPrep_(self.symbol, period="quarter", call="income_statement")
        for e in range(0, len(income_statement_quarter)):
            d_incomeStatement = {}
            for k in income_statement_quarter[e].keys():
                d_incomeStatement[k] = income_statement_quarter[e][k]

            # Add to revenueQuarter
            year = income_statement_quarter[e]["date"][0:4]
            quarter = income_statement_quarter[e]["period"]
            rev = income_statement_quarter[e]['revenue']
            period = "{Y}-{Q}".format(Y=year, Q=quarter)
            self.revenueQuarter.loc[e] = [period, rev]

            # just use year for indexing -> [0:4]
            if year not in fundamentals["income_statement"]:
                fundamentals["income_statement"][year] = {}
            fundamentals["income_statement"][year][quarter] = d_incomeStatement

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

        # save dictionary to data-folder
        if save:
            with open("data/" + self.symbol + ".json", 'w') as file:
                # Serialize data into file:
                json.dump(fundamentals, file)
        return fundamentals
