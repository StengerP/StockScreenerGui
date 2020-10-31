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

        # Initialized in self._init_data()
        # TODO maybe use DF_xxx instead of fundamentalsAnnual/Quarter & growthAnnual in future
        self.DF_fundamentalsAnnual = pd.DataFrame()
        self.DF_fundamentalsQuarter = pd.DataFrame()
        self.DF_growthAnnual = pd.DataFrame()
        #self.DF_growthQuarter = pd.DataFrame()

        self.data = self._init_data()
        self.chart_onePerDay = self._load_chartHistory(period='1d')


        # TODO tbd - daily charts with 1min, 5min, ..., 1h, 4h intervalls
        #self.chart_daily = self._load_chartHistory(XXX)

        Stock.n_stocks += 1


    @classmethod
    def counter(cls):
        return cls.n_stocks

    def _load_chartHistory(self, period='1d'):
        if period == '1d':
            hist = Stock.API.callAPI_financialModelingPrep_(self.symbol, call="dailychart")
        return pd.DataFrame(hist['historical'])

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
        self.DF_fundamentalsAnnual = pd.DataFrame(income_statement)
        for e in range(len(income_statement)-1, -1, -1):
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
            #self.revenueAnnual.loc[e] = [year, rev]
            self.fundamentalsAnnual.loc[e] = [timestamp, year, rev, grossprofit, opincome, netprofit,
                                              grMargin, opMargin, netMargin]
            # just use year for indexing -> [0:4]
            if year not in data["income_statement"]:
                data["income_statement"][year] = {}
            data["income_statement"][year]["Annual"] = d_incomeStatement

        #calculate growth (load from API)
        income_statement_growth = Stock.API.callAPI_financialModelingPrep_(self.symbol, call="growth")
        self.DF_growthAnnual = pd.DataFrame(income_statement_growth)
        for e in range(0, len(income_statement_growth)):
            revGrowth = income_statement_growth[e]['growthRevenue']
            profitGrowth = income_statement_growth[e]['growthNetIncome']
            self.growthAnnual.loc[e] = [income_statement_growth[e]['date'], revGrowth, profitGrowth]


        # Quarters
        income_statement_quarter = Stock.API.callAPI_financialModelingPrep_(self.symbol, period="quarter", call="income_statement")
        self.DF_fundamentalsQuarter = pd.DataFrame(income_statement_quarter)
        'revenue', 'grossProfit', 'operatingIncome', 'netProfit',
        'grossMargin', 'operatingMargin', 'profitMargin'

        timestamp_TTM, rev_TTM, grossProfit_TTM, operatingIncome_TTM, netProfit_TTM = 0, 0, 0, 0, 0,
        c_quarters = 0
        for e in range(len(income_statement_quarter)-1, -1, -1):
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
            #self.revenueQuarter.loc[e] = [period, rev]
            self.fundamentalsQuarter.loc[e] = [timestamp, period, rev, grossprofit, opincome, netprofit,
                                               grMargin, opMargin, netMargin]

            # just use year for indexing -> [0:4]
            if year not in data["income_statement"]:
                data["income_statement"][year] = {}
            data["income_statement"][year][quarter] = d_incomeStatement

            #TTM data (last 4 quarters)
            if e < 4:
                if e == 0:
                    timestamp_TTM = timestamp
                rev_TTM += rev
                grossProfit_TTM += grossprofit
                operatingIncome_TTM += opincome
                netProfit_TTM += netprofit
                #c_quarters += 1
        # TODO add TTM at the beginning of the Dataframe. Maybe solve problem with indexing 0 -> 2017 1->2018 2 -> 2019 3->TTM
        self.fundamentalsAnnual.loc[5] = [timestamp_TTM, 'TTM', rev_TTM, grossProfit_TTM, operatingIncome_TTM,
                                           netProfit_TTM, grossProfit_TTM/rev_TTM, operatingIncome_TTM/rev_TTM, netProfit_TTM/rev_TTM]

        #calculate growth
        for e in range(len(self.fundamentalsQuarter)-1, -1, -1):
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

    def kgv(self):

        pass

    # Get Methods
    def get_fundamentalsAnnual(self):
        return self.fundamentalsAnnual

    def get_fundamentalsQuarter(self):
        return self.fundamentalsQuarter

    def get_growthAnnual(self):
        return self.fundamentalsAnnual

    def get_growthQuarter(self):
        return self.fundamentalsQuarter
