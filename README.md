# FinancialDataIngestion
Repo for processing documents from the US SEC api

This repository is currently set up to be a script for retrieving, formatting and downloading historical financial data for a single company.

### TODO:
Set up the repository to be a package that can be installed.

# Use
```py
# ~~~~~~~~~~~~~~~~~~~
#       INPUTS
# ~~~~~~~~~~~~~~~~~~~
# This will collect the past 3 years of data from yfinance
# and will collect all data for the [TICKER] from the SEC
TICKER = "GOOGL"

# Whether to download a filtered SEC document (filtered with ["label", "end", "form", "fp"] as the unique key)
DOWNLOAD_FILTERED = True
# ~~~~~~~~~~~~~~~~~~~
#       
# ~~~~~~~~~~~~~~~~~~~
```
To download data for a specific company in the United States, replace string for the `TICKER` variable with your desired company ticker. This will download `[TICKER]_SEC.csv`, and `[TICKER]_yfinance.csv`.

`EXPERIMENTAL`: If `DOWNLOAD_FILTERED=True`, the file `[TICKER_SEC_filtered.csv]` will be downloaded. This file filters out duplicate filings from the SEC API filed on different dates.

# Data Sources
We collect `Date, Open, High, Low, Close, Volume, Dividends, Stock Splits` from the [`yfinance`](https://github.com/ranaroussi/yfinance) package, which queries the Yahoo Finance API.

To collect company information data we query the [SEC EDGAR API](https://www.sec.gov/edgar/sec-api-documentation). This information is free from a branch of the United States Government.
