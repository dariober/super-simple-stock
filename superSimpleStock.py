#!/usr/bin/env python3

import pandas
import re
import math
import datetime
import dateutil 

class Stock:
    """Class modeling the Super Simple Stock as described in the assignment.
    This implementation favours simplicity over efficiency and
    comprehensiveness. 
    
    The Stock object is constructed from a csv file of stock data. See
    sample_data.csv for an example and superSimpleStockTest.py for test cases.
    """
    def __init__(self, csv_file):
        self.gbce_data= self._read_stock_data(csv_file)
        self.trade= pandas.DataFrame({'Stock_Symbol': [], 'timestamp': [], 'quantity': [], 'sold': [], 'price': []})

    def get_dividend_yield(self, stock, ticker_price):
        """Answers the exercise question 'i. Calculate the dividend yield'
        """
        dstock= self.gbce_data[self.gbce_data['Stock_Symbol'] == stock]
        if len(dstock['Type']) != 1:
            raise Exception('Too many or no values for\n%s' % stock)

        if list(dstock['Type'])[0] == 'Common':
            return list(dstock['Last_Dividend'])[0] / ticker_price
        elif list(dstock['Type'])[0] == 'Preferred':
            return (list(dstock['Fixed_Dividend'])[0] * list(dstock['Par_Value'])[0]) / ticker_price
        else:
            raise Exception('Unexpected stock type:\n%s' % dstock['Type'])

    def get_pe_ratio(self, stock, ticker_price):
        """Answers question 'ii. Calculate the P/E Ratio'
        """
        dividend= self.get_dividend_yield(stock, ticker_price)
        if dividend == 0:
            return float('nan')
        return ticker_price / dividend

    def record_trade(self, stock, quantity, sold, price):
        """Answers question 'iii. Record a trade, with timestamp, quantity of
        shares, buy or sell indicator and price'
        
        Record the trade of the given stock and append it to the trade
        dataframe. 
        
        sold: boolean. If True, the stock has been sold. If False, it has been
        bought
        """
        if stock not in set(self.gbce_data['Stock_Symbol']):
            raise Exception('Unknown stock: %s' % stock)

        trade= {'Stock_Symbol': stock,
                'timestamp': datetime.datetime.now().isoformat(), 
                'quantity': quantity,
                'sold': sold,
                'price': price}
        self.trade= self.trade.append(trade, ignore_index= True)

    def get_stock_price(self, stock, last_minutes= 15):
        """Answers question 'iii. Calculate Stock Price based on trades
        recorded in past 15 minutes'
        
        Return the price of the given stock on the basis of the transactions
        recorded in the last `last_minutes`. Return NaN if no transactions are
        available.
        """
        since= datetime.datetime.now() - datetime.timedelta(minutes= last_minutes)
        
        if len(self.trade) == 0:
            return float('nan')

        tstock= self.trade[self.trade['Stock_Symbol'] == stock]
        if len(tstock) == 0:
            return float('nan')

        last_trades= [ dateutil.parser.parse(x) > since for x in list(tstock['timestamp']) ]

        tstock= tstock[last_trades]
        if len(tstock) == 0:
            return float('nan')

        ## NB: This includes both sold and bought trades
        return sum(tstock['price'] * tstock['quantity']) / sum(tstock['quantity'])

    def get_all_share_index(self):
        """Answers question 'b. Calculate the GBCE All Share Index using the
        geometric mean of prices for all stocks'
        """
        if len(self.trade) == 0:
            return float('nan')
        all_share_index= 1
        n= 0
        for p in list(self.trade['price']):
            # It would be better to do a sum of logs as this product could go
            # in numeric overflow
            all_share_index *= p
            n += 1
        return all_share_index ** (1 / n)

    def _read_stock_data(self, csv_file):
        """Read the given csv file and return a cleaned dataframe
        """
        gbce_data= pandas.read_csv(csv_file)
        fixed_dividend= []
        for x in gbce_data['Fixed_Dividend']: 
            # Convert the strings 'd%' to numeric unless the cell value is NaN.
            if type(x) == float and math.isnan(x):
                pass
            else:
                try:
                    x= float(re.sub('%$', '', x)) / 100
                except:
                    raise('Cannot convert %s to numeric' % x)
            fixed_dividend.append(x)
        gbce_data['Fixed_Dividend']= fixed_dividend
        return gbce_data


