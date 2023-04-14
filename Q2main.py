import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CO2_df = pd.read_csv("owid-co2-data.csv")
CO2_df.dropna(subset=["iso_code"], inplace=True)
CO2_backup_df = CO2_df.copy()


CO2_df.dropna(subset=["co2"], inplace=True)
CO2_df["CO2 per capita"] = CO2_df["co2"] / CO2_df["population"]

CO2_strides_df = CO2_df[["country", "year", "CO2 per capita"]]

for country in CO2_strides_df["country"].unique():
    mask = CO2_strides_df["country"] == country
    CO2_strides_df.loc[mask, "Yearly % change"] = CO2_strides_df.loc[mask, "CO2 per capita"].pct_change() * 100

decade_bins = pd.IntervalIndex.from_tuples([(1950, 1959), (1960, 1969), (1970, 1979), (1980, 1989), (1990, 1999), (2000, 2009), (2010, 2021)], closed="left")
CO2_strides_df["decade"] = pd.cut(CO2_strides_df["year"], bins=decade_bins, labels=["1950-1959", "1960-1969", "1970-1979", "1980-1989", "1990-1999", "2000-2009", "2010-2021"])
grouped = CO2_strides_df.groupby(["country", "decade"])["Yearly % change"].agg(["mean", "max", "min"])
grouped.replace([np.inf, -np.inf], np.nan, inplace=True)
grouped.dropna(inplace=True)

# Part 1
countries = ["China", "Italy", "United States"]
grouped_countries = grouped.loc[countries]

for country in countries:
    plt.figure()
    plt.title(country)
    country_data = grouped_countries.loc[country]
    x = range(len(decade_bins))
    plt.plot(x, country_data["mean"], label="mean")
    plt.plot(x, country_data["max"], label="max")
    plt.plot(x, country_data["min"], label="min")
    plt.xticks(x, decade_bins, rotation=45)
    plt.legend()
    plt.show()


# Part 2
grouped.reset_index(inplace=True)
decade_filter = pd.Interval(2010, 2021, closed='left')
mean_sorted = grouped.sort_values("mean", ascending=True)
filtered = mean_sorted[mean_sorted["decade"].isin([decade_filter])]
mean_top_countries = list(filtered["country"].head(5))
print(f"When it comes to mean yearly change, the best countries are: {mean_top_countries}")
min_sorted = grouped.sort_values("min", ascending=True)
filtered = min_sorted[min_sorted["decade"].isin([decade_filter])]
min_top_countries = list(filtered["country"].head(5))
print(f"When it comes to maximum yearly decline, the best countries are: {min_top_countries}")

# Part 3

CO2_2021 = CO2_strides_df[CO2_strides_df['year'] == 2021]
CO2_2021_sorted = CO2_2021.sort_values("CO2 per capita", ascending=False)
top_20_polluters = CO2_2021_sorted.head(20)["country"].tolist()


grouped.reset_index(inplace=True)
grouped = grouped[grouped["country"].isin(top_20_polluters)]
decade_filter = pd.Interval(2010, 2021, closed='left')
mean_sorted = grouped.sort_values("mean", ascending=True)
filtered = mean_sorted[mean_sorted["decade"].isin([decade_filter])]
mean_top_countries = list(filtered["country"].head(5))
print(f"When it comes to mean yearly change, among the top 20 big polluters the best countries are: {mean_top_countries}")
min_sorted = grouped.sort_values("min", ascending=True)
filtered = min_sorted[min_sorted["decade"].isin([decade_filter])]
min_top_countries = list(filtered["country"].head(5))
print(f"When it comes to maximum yearly decline, among the top 20 big polluters the best countries are: {min_top_countries}")
