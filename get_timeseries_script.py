import json
import pandas as pd
import requests
from sec_cik_mapper import StockMapper
import yfinance as yf

# ~~~~~~~~~~~~~~~~~~~
#       INPUTS
# ~~~~~~~~~~~~~~~~~~~
TICKER = "AAPL"
DATES = ()
# ~~~~~~~~~~~~~~~~~~~
#       INPUTS
# ~~~~~~~~~~~~~~~~~~~


tkr = yf.Ticker(TICKER)

mapper = StockMapper()
cik = mapper.ticker_to_cik[TICKER]


headers = {"User-Agent": "stirlingjamessmith@gmail.com"}
api_url = 'https://data.sec.gov/api/xbrl/companyfacts/CIK{}.json'.format(cik)

response = requests.get("https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json", headers=headers).text
contents = json.loads(response)

company_name = contents["entityName"]

labeled_dicts = contents["facts"]["us-gaap"]
labels = list(labeled_dicts.keys())

labeled_dicts_small = contents["facts"]["dei"]
labels_small = list(labeled_dicts_small.keys())

def labeled_to_df(labeled_dicts, label):

    units = list(labeled_dicts[label]["units"].keys())
    dfs = []
    def filter_dict(dicts, k): return [dict[k] for dict in dicts]

    for u in units:
        share_updates = labeled_dicts[label]["units"][u]
        keys = ["val", "filed", "form", "end", "fp"]

        dicts = [{k: filter_dict(share_updates, k)} for k in keys]
        unit_df=pd.DataFrame({**dicts[0], **dicts[1], **dicts[2], **dicts[3], **dicts[4]})

        #println(share_updates)
        # unit_df = vcat(DataFrame.(share_updates)...)
        unit_df["label"]=label
        unit_df["unit"]=u
        dfs.append(unit_df)
    
    return pd.DataFrame(pd.concat(dfs))

dfs = pd.concat([labeled_to_df(labeled_dicts, l) for l in labels])
dfs_small = pd.concat([labeled_to_df(labeled_dicts_small, l) for l in labels_small])

big_df = pd.concat([dfs, dfs_small])

filtered_big_df = big_df.groupby(["label", "end", "form", "fp"]).head(1)


#### YFinance

with open("{}_yfinance.csv".format(TICKER), "w") as f:
    f.write(tkr.history(period="3y").to_csv())


with open("{}_SEC.csv".format(TICKER), 'w') as f:
    f.write(filtered_big_df.to_csv(index=False))

with open("{}_SEC_big.csv".format(TICKER), 'w') as f:
    f.write(big_df.to_csv(index=False))