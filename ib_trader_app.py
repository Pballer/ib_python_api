from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum

import threading

import sqlite3

#import pandas as pd


class MarketDataApp(EWrapper, EClient):

    def __init__(self, dbConn):
        EClient.__init__(self, self)
        self.dbConn = dbConn

    def error(self, reqId, errorCode, errorString):
        print("Error ", reqId, " ", errorCode, " ", errorString)

    def contractDetails(self, reqId, contractDetails):
        print("contractDetails: ", reqId, " ", contractDetails)

    def tickPrice(self, reqId , tickType, price, attrib):
        insertSql = """
            insert into tick_market_data
            values ({tickerId}, CURRENT_TIMESTAMP, "{tickType}", {price})
            """.format(tickerId=reqId,
                       tickType=TickTypeEnum.to_str(tickType),
                       price=price)
        #print(insertSql)
        print('tickSize: ', reqId, TickTypeEnum.to_str(tickType))
        self.dbConn.execute(insertSql)
        self.dbConn.commit()

        # print("Tick Price. Ticker Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType),
        #       "Price:", price)

    def tickSize(self, reqId, tickType, size):
        insertSql = """
                    insert into tick_market_data
                    values ({tickerId}, CURRENT_TIMESTAMP, "{tickType}", {price})
                    """.format(tickerId=reqId,
                               tickType=TickTypeEnum.to_str(tickType),
                               price=size)
        #print(insertSql)
        print('tickSize: ', reqId, TickTypeEnum.to_str(tickType))
        self.dbConn.execute(insertSql)
        self.dbConn.commit()

        #print("Tick Size. Ticker Id:", reqId, "tickType", TickTypeEnum.to_str(tickType),
        #      "Size:", size)

    def historicalData(self, reqId, bar):
        insertSql = """
            insert into historical_market_data
            values ({tickerid}, CURRENT_TIMESTAMP, {high}, {low}, {open}, {close})
            """.format(tickerid=reqId,
                       #date=bar.date,
                       high=bar.high,
                       low=bar.low,
                       open=bar.open,
                       close=bar.close)

        self.dbConn.execute(insertSql)
        self.dbConn.commit()

    #def newsArticle(self, requestId:int, articleType:int, articleText:str):

    def historicalNews(self, requestId, time, providerCode, articleId, headline):
        print(requestId, time, providerCode, articleId, headline)

    def newsArticle(self, requestId, articleType, articleText):
        print(requestId, articleType, articleText)


def simpleStockContract():
    contract = Contract()
    contract.symbol = "NUGT"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "NYSE"
    return contract


def optContract():
    contract = Contract()
    contract.symbol = 'GOOG'
    contract.secType = 'OPT'
    contract.exchange = 'SMART'
    contract.currency = 'USD'
    contract.lastTradeDateOrContractMonth = '20190823'
    contract.strike = 1190
    contract.right = 'C'
    contract.multiplier = '100'
    return contract

def getCcyPairContract():
    contract = Contract()
    contract.symbol = 'EUR'
    contract.secType = 'CASH'
    contract.exchange = 'IDEALPRO'
    contract.currency = 'USD'
    return contract


def main():

    try:
        db_conn = sqlite3.connect('./db/ib_api.db')
    except Exception as e:
        print(e)
        raise e

    app = MarketDataApp(db_conn)

    app.connect("127.0.0.1", 7497, 0)
    app.reqMarketDataType(4)  # 4 is delayed-frozen data.  Use this if not subscribed to live or after market hours.


    smpl_stk_contract = simpleStockContract()
    opt_contract = optContract()

    app.reqMktData(1, smpl_stk_contract, "", False, False, [])  # NUGT
    #app.reqHistoricalData()

    dust_contract = simpleStockContract()  # DUST
    dust_contract.symbol = 'DUST'
    app.reqMktData(2, dust_contract, "", False, False, [])

    #app.reqContractDetails(1, smpl_stk_contract)

    #ccyPairContract = getCcyPairContract()

    # Historical data
    #app.reqHistoricalData(1, ccyPairContract, '20190701 09:00:00 EST', '1 D', '1 day', 'BID_ASK', 0, 1, False, [])


    # News
    #app.reqHistoricalNews(10003, 8314, "BRFG", "", "", 10, [])
    #app.reqNewsArticle(10002, "BRFG", "BRFG$0b37971a", [])

    app.run()


if __name__ == "__main__":
    main()
