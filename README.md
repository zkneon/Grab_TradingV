<div align="center">

# Grab Stock Data from TradingView

[![Python](https://img.shields.io/badge/Python-3.9-blue?style=flat&logo=python)]()
[![WebSocket](https://img.shields.io/badge/WebSocket-red?style=flat&logo=python)]()
[![Pandas](https://img.shields.io/badge/Pandas-red?style=flat&logo=pandas)]()

</div>

## Information

Grab stock data from TradingView.

Get data for 5 years ago, timeframe one day.
If you want change this, you need use this variables:

```py
TIME_FRAME = "1D"   # minute( 3, 5, 15, 30, 60, 120, 1D)
CANDELS = 300
WIDTH_FRAME = '60M'  # (12, 60M)

```

Change this list for get another stock:

```py
# List of stock name with market name
stock_list = ["MOEX:SBER", "MOEX:LKOH"]

```

Add login and password from TradingView account to /.env file.



