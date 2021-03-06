[![Build & Test Status](https://travis-ci.com/dariober/super-simple-stock.svg?branch=master)](https://travis-ci.com/dariober/super-simple-stock)

The code for the *Super Simple Stock* exercise is in `superSimpleStock.py`.
Tests and test data are in `test/superSimpleStockTest.py` and `test/sample_data.csv`
respectively.

# Dependencies

* Python 3.x

* Additional modules not in the standard library can be installed with:

```
pip install python-dateutil
pip install pandas
```

# Usage example

```
import superSimpleStock

stock= superSimpleStock.Stock('test/sample_data.csv')

stock.get_dividend_yield(stock= 'POP', ticker_price= 3)

stock.get_pe_ratio(stock= 'POP', ticker_price= 3)

stock.record_trade(stock= 'POP', quantity= 10, sold= True, price= 5)
stock.record_trade(stock= 'POP', quantity= 11, sold= True, price= 6)
stock.record_trade(stock= 'POP', quantity= 12, sold= True, price= 7)
print(stock.trade)

stock.get_stock_price('POP')

stock.get_all_share_index()
```

# Run tests

```
python3 -m unittest test.superSimpleStockTest
```

If [coverage](https://coverage.readthedocs.io/en/coverage-4.5.1a/) is
installed, run tests and report coverage with:

```
coverage run -m unittest test.superSimpleStockTest
coverage html --include='superSimpleStock*'
```

Coverage report will be in [htmlcov](htmlcov/index.html)

Or:

```
coverage report --include='superSimpleStock*'

Name                  Stmts   Miss  Cover
-----------------------------------------
superSimpleStock.py      64      3    95%
```

----

Author: Dario Beraldi

Date: 19/09/2018
