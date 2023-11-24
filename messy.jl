using JSON
using Dates
using PlotlyJS

doc = JSON.parsefile("SampleSECData/CIK0000002488.json")
company_name = doc["entityName"]
share_updates = doc["facts"]["dei"]["EntityCommonStockSharesOutstanding"]["units"]["shares"]

val_from_dict(d, key) = d[key]

dates = val_from_dict.(share_updates, ["filed"])
dates = Date.(dates)

outstanding_shares = val_from_dict.(share_updates, "val")
plot(dates, outstanding_shares, Layout(title=string("Outstanding shares across time: ",company_name)))

using HTTP
api_response = HTTP.get(string("https://api.iex.cloud/v1/data/core/historical_prices/aem?range=2y&token=",ENV["IEXTOKEN"]))

output = JSON.parse(String(api_response.body))

JSON.write("AGNICO_EAGLE_MINES.json", JSON.json(output))