import json
import pandas as pd
import requests
from sec_cik_mapper import StockMapper
import yfinance as yf

# ~~~~~~~~~~~~~~~~~~~
#       INPUTS
# ~~~~~~~~~~~~~~~~~~~
# This will collect the past 3 years of data from yfinance
# and will collect all data for the [TICKER] from the SEC
TICKER = "ZYXI"

# Whether to download a filtered SEC document (filtered with ["label", "end", "form", "fp"] as the unique key)
DOWNLOAD_FILTERED = True
# ~~~~~~~~~~~~~~~~~~~
#       
# ~~~~~~~~~~~~~~~~~~~


tkr = yf.Ticker(TICKER)

mapper = StockMapper()
cik = mapper.ticker_to_cik[TICKER]


headers = {"User-Agent": "stirlingjamessmith@gmail.com"}
api_url = 'https://data.sec.gov/api/xbrl/companyfacts/CIK{}.json'.format(cik)

response = requests.get(api_url, headers=headers).text
contents = json.loads(response)

company_name = contents["entityName"]

print("Downloading Data for",company_name)

# SEC Data is split into 2 sections us-gaap and dei
labeled_dicts_gaap = contents["facts"]["us-gaap"]
labels_gaap = list(labeled_dicts_gaap.keys())

labeled_dicts_dei = contents["facts"]["dei"]
labels_dei = list(labeled_dicts_dei.keys())

def labeled_to_df(labeled_dicts, label):

    units = list(labeled_dicts[label]["units"].keys())
    dfs = []
    def filter_dict(dicts, k): return [dict[k] for dict in dicts]

    for u in units:
        sample_dict = labeled_dicts[label]["units"][u]
        keys = ["val", "filed", "form", "end", "fp"]

        dicts = [{k: filter_dict(sample_dict, k)} for k in keys]
        unit_df=pd.DataFrame({**dicts[0], **dicts[1], **dicts[2], **dicts[3], **dicts[4]})

        unit_df["label"]=label
        unit_df["unit"]=u
        dfs.append(unit_df)
    
    return pd.DataFrame(pd.concat(dfs))

df_gaap = pd.concat([labeled_to_df(labeled_dicts_gaap, l) for l in labels_gaap])
dfs_dei = pd.concat([labeled_to_df(labeled_dicts_dei, l) for l in labels_dei])

# joining both us-gaap and dei dataframes
big_df = pd.concat([df_gaap, dfs_dei])

filtered_big_df = big_df.groupby(["label", "end", "form", "fp"]).head(1)



with open("{}_yfinance.csv".format(TICKER), "w") as f:
    f.write(tkr.history(period="3y").to_csv())

if DOWNLOAD_FILTERED:
    with open("{}_SEC_filtered.csv".format(TICKER), 'w') as f:
        f.write(filtered_big_df.to_csv(index=False))

with open("{}_SEC.csv".format(TICKER), 'w') as f:
    f.write(big_df.to_csv(index=False))