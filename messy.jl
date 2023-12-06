using CSV
using JSON
using Dates
using DataFrames
using PlotlyJS

doc = JSON.parsefile("SampleSECData/CIK0000001750.json")
company_name = doc["entityName"]


labeled_dicts = doc["facts"]["us-gaap"]
labels = collect(keys(labeled_dicts))

labeled_dicts = doc["facts"]["dei"]
labels = collect(keys(labeled_dicts))

function labeled_to_df(labeled_dicts, label)
    println(label)
    units = collect(keys(labeled_dicts[label]["units"]))
    dfs = []
    filter_dict(dict, k) = dict[k]
    for u in units
        share_updates = labeled_dicts[label]["units"][u]
        keys = ["val", "filed", "form", "end"]
        unit_df=DataFrame([k=>filter_dict.(share_updates, [k]) for k in keys])
        #println(share_updates)
        # unit_df = vcat(DataFrame.(share_updates)...)
        unit_df.label.=label
        unit_df.unit.=u
        push!(dfs,unit_df)
    end
    return vcat(dfs...)
end

dfs_low = vcat(labeled_to_df.([labeled_dicts], labels)...)
dfs = vcat(labeled_to_df.([labeled_dicts], labels)...)
CSV.write("SEC_reformated_data.csv", vcat(dfs, dfs_low))

labeled_dicts[labels[3]]["units"]["shares"][end]["val", "filed", "form"]
key_sets = unique((keys.(labeled_dicts[labels[3]]["units"]["shares"])))
all_keys = unique(vcat(collect.(key_sets)...))
sum(keys.(labeled_dicts[labels[3]]["units"]["shares"]).==[key_sets[2]])


val_from_dict(d, key) = d[key]

dates = val_from_dict.(share_updates, ["filed"])
dates = Date.(dates)

outstanding_shares = val_from_dict.(share_updates, "val")
plot(dates, outstanding_shares, Layout(title=string("Outstanding shares across time: ",company_name)))


# using HTTP
# api_response = HTTP.get(string("https://api.iex.cloud/v1/data/core/historical_prices/amzn?range=1y&token=",ENV["qIEXTOKEN"]))

# output = JSON.parse(String(api_response.body))

# JSON.write("amazon.json", JSON.json(output))


prices = JSON.parsefile("AAR_Corp_prices.json")

dfs = DataFrame.(prices)

bigdf = vcat(dfs...)

filtered_bigdf = bigdf[:, [:symbol, :open, :close, :high, :low, :volume]]

CSV.write("AAR_price_filtered.csv",filtered_bigdf)


sec = CSV.read("SEC_reformated_data.csv", DataFrame)

assets = sec[sec.label.=="Assets",:]

k10 = assets[assets.form.=="10-K",:][1:7,:]

k10[3:5,:].val

using HTTP
HTTP.get("https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json")