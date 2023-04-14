import pandas as pd
from scipy.stats import pearsonr

CO2_df = pd.read_csv("owid-co2-data.csv")
CO2_df.dropna(subset=["iso_code"], inplace=True)
CO2_backup_df = CO2_df.copy()

CO2_df.dropna(subset=["co2", "gdp"], inplace=True)
corr, p_value = pearsonr(CO2_df["co2"], CO2_df["gdp"])

print(f"Pearson correlation coefficient bewteen total C02 emissions and total GDP: {corr}. P-value: {p_value}")

CO2_df["CO2 per capita"] = CO2_df["co2"] / CO2_df["population"]
CO2_df["GDP per capita"] = CO2_df["gdp"] / CO2_df["population"]
CO2_df.dropna(subset=["CO2 per capita", "GDP per capita"], inplace=True)
corr, p_value = pearsonr(CO2_df["CO2 per capita"], CO2_df["GDP per capita"])

print(f"Pearson correlation coefficient between CO2 emisisons per capita and GDP per capita: {corr}. P-value: {p_value}")

diet_df = pd.read_csv("dietary-compositions-by-commodity-group.csv")
diet_df["Total intake in Kilocalories"] = diet_df.iloc[:, 3:13].sum(axis=1)
diet_df["% of calories from meat"] = (diet_df["Meat (FAO (2017)) (kilocalories per person per day)"] / diet_df["Total intake in Kilocalories"]) * 100


CO2_and_diet_df = CO2_backup_df.loc[:, ["country", "year", "co2", "population"]]
CO2_and_diet_df.dropna(subset=["co2"], inplace=True)
CO2_and_diet_df["CO2 per capita"] = CO2_and_diet_df["co2"] / CO2_and_diet_df["population"]

CO2_and_diet_df["Meat (FAO (2017)) (kilocalories per person per day)"] = ""
CO2_and_diet_df["% of calories from meat"] = ""


for index, row in CO2_and_diet_df.iterrows():
    country = row["country"]
    year = row["year"]
    diet_value_meat = diet_df.loc[(diet_df["Entity"] == country) & (diet_df["Year"] == year), "Meat (FAO (2017)) (kilocalories per person per day)"].values
    diet_value_percent = diet_df.loc[(diet_df["Entity"] == country) & (diet_df["Year"] == year), "% of calories from meat"].values

    if len(diet_value_meat) > 0:
        CO2_and_diet_df.at[index, "Meat (FAO (2017)) (kilocalories per person per day)"] = diet_value_meat[0]

    if len(diet_value_percent) > 0:
        CO2_and_diet_df.at[index, "% of calories from meat"] = diet_value_percent[0]

CO2_and_diet_df["Meat (FAO (2017)) (kilocalories per person per day)"] = pd.to_numeric(CO2_and_diet_df["Meat (FAO (2017)) (kilocalories per person per day)"], errors='coerce')
CO2_and_diet_df.dropna(subset=["CO2 per capita", "Meat (FAO (2017)) (kilocalories per person per day)"], inplace=True)
corr, p_value = pearsonr(CO2_and_diet_df["CO2 per capita"], CO2_and_diet_df["Meat (FAO (2017)) (kilocalories per person per day)"])
print(f"Pearson correlation coefficient between CO2 emisisons per capita and individual intake of Kilocalories from meat: {corr}. P-value: {p_value}")


corr, p_value = pearsonr(CO2_and_diet_df["CO2 per capita"], CO2_and_diet_df["% of calories from meat"])
print(f"Pearson correlation coefficient between CO2 emisisons per capita and % of Kilocalories from meat: {corr}. P-value: {p_value}")
