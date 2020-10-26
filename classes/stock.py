from financeAPI.financeAPI_lib import FinanceAPI as fapi
from pathlib import Path
import json
import pandas as pd

class Stock:

    n_stocks = 0
    API = fapi()

    def __init__(self, symbol:str):
        self.symbol = symbol
        self.fundamentalsAnnual = pd.DataFrame(columns=['time', 'year', 'revenue', 'grossProfit', 'operatingIncome', 'netProfit',
                                                        'grossMargin', 'operatingMargin', 'profitMargin'])
        self.fundamentalsQuarter = pd.DataFrame(columns=['time', 'quarter', 'revenue', 'grossProfit', 'operatingIncome', 'netProfit',
                                                         'grossMargin', 'operatingMargin', 'profitMargin'])
        self.growthAnnual = pd.DataFrame(columns=['time', 'revGrowth', 'profitGrowth'])
        self.growthQuarter = pd.DataFrame(columns=['time', 'revGrowth', 'profitGrowth'])
        self.revenueAnnual = pd.DataFrame(columns=['year', 'revenue'])
        self.revenueQuarter = pd.DataFrame(columns=['quarter', 'revenue'])
        self.data = self._init_data()
        self.chart = self._load_chartHistory()
        Stock.n_stocks += 1

    @classmethod
    def counter(cls):
        return cls.n_stocks

    def _load_chartHistory(self):
        pass

    def _init_data(self, save=False):

        data = {}

        if Stock.API.key_registered == False:
            # Check for API Key and load
            if Path("financeAPI/Secret_Key.txt").is_file():
                with open('financeAPI/Secret_Key.txt') as file:
                    key = file.read()
                Stock.API.registerKey_(key)
            else:
                print("No file with API key found")
                exit()

        data['symbol'] = self.symbol
        # self.metrics_data_(self.symbol)
        # self.ratios_data_(self.symbol)

        """
        profile data
        """
        profile = Stock.API.callAPI_financialModelingPrep_(self.symbol, call="profile")
        data["profile"] = {}
        d_profile = {}
        for k in profile.keys():
            d_profile[k] = profile[k]
            data["profile"] = d_profile

        """
        income statement data
        """
        data["income_statement"] = {}

        # Annual
        income_statement = Stock.API.callAPI_financialModelingPrep_(self.symbol, call="income_statement")
        for e in range(0, len(income_statement)):
            d_incomeStatement = {}
            for k in income_statement[e].keys():
                d_incomeStatement[k] = income_statement[e][k]

            # Add to revenueAnnual
            timestamp = income_statement[e]["date"]
            year = income_statement[e]["date"][0:4]
            rev = income_statement[e]['revenue']
            grossprofit = income_statement[e]['grossProfit']
            opincome = income_statement[e]['operatingIncome']
            netprofit = income_statement[e]['netIncome']
            grMargin = income_statement[e]['grossProfitRatio']
            opMargin = income_statement[e]['operatingIncomeRatio']
            netMargin = income_statement[e]['netIncomeRatio']
            # TODO Add Cost-Numbers (R&D, Sales etc.)
            self.revenueAnnual.loc[e] = [year, rev]
            self.fundamentalsAnnual.loc[e] = [timestamp, year, rev, grossprofit, opincome, netprofit,
                                              grMargin, opMargin, netMargin]

            # just use year for indexing -> [0:4]
            if year not in data["income_statement"]:
                data["income_statement"][year] = {}
            data["income_statement"][year]["Annual"] = d_incomeStatement

        #calculate growth (load from API)
        income_statement_growth = Stock.API.callAPI_financialModelingPrep_(self.symbol, call="growth")
        for e in range(0, len(income_statement_growth)):
            revGrowth = income_statement_growth[e]['growthRevenue']
            profitGrowth = income_statement_growth[e]['growthNetIncome']
            self.growthAnnual.loc[e] = [income_statement_growth[e]['date'], revGrowth, profitGrowth]


        # Quarters
        income_statement_quarter = Stock.API.callAPI_financialModelingPrep_(self.symbol, period="quarter", call="income_statement")
        for e in range(0, len(income_statement_quarter)):
            d_incomeStatement = {}
            for k in income_statement_quarter[e].keys():
                d_incomeStatement[k] = income_statement_quarter[e][k]

            # Add to revenueQuarter
            timestamp = income_statement_quarter[e]["date"]
            year = income_statement_quarter[e]["date"][0:4]
            quarter = income_statement_quarter[e]["period"]
            rev = income_statement_quarter[e]['revenue']
            grossprofit = income_statement_quarter[e]['grossProfit']
            opincome = income_statement_quarter[e]['operatingIncome']
            netprofit = income_statement_quarter[e]['netIncome']
            grMargin = income_statement_quarter[e]['grossProfitRatio']
            opMargin = income_statement_quarter[e]['operatingIncomeRatio']
            netMargin = income_statement_quarter[e]['netIncomeRatio']
            # TODO Add Cost-Numbers (R&D, Sales etc.)
            period = "{Y}-{Q}".format(Y=year, Q=quarter)
            self.revenueQuarter.loc[e] = [period, rev]
            self.fundamentalsQuarter.loc[e] = [timestamp, period, rev, grossprofit, opincome, netprofit,
                                               grMargin, opMargin, netMargin]

            # just use year for indexing -> [0:4]
            if year not in data["income_statement"]:
                data["income_statement"][year] = {}
            data["income_statement"][year][quarter] = d_incomeStatement

        #calculate growth
        for e in range(0, len(self.fundamentalsQuarter)):
           if not e == self.fundamentalsQuarter.shape[0]-1: # Anzahl Zeilen des Dataframes
               revGrowth = (self.fundamentalsQuarter.iloc[e]['revenue'] / self.fundamentalsQuarter.iloc[e+1]['revenue'])-1
               profitGrowth = (self.fundamentalsQuarter.iloc[e]['netProfit'] / self.fundamentalsQuarter.iloc[e+1]['netProfit'])-1
           else:
               revGrowth = 0
               profitGrowth = 0
           self.growthQuarter.loc[e] = [self.fundamentalsQuarter.iloc[e]['time'], revGrowth, profitGrowth]

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
                json.dump(data, file)
        return data
