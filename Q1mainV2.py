import pandas as pd
from scipy.stats import pearsonr, linregress
import matplotlib.pyplot as plt

# Read the CSV file from the GitHub URL and create the DataFrame
url = "https://raw.githubusercontent.com/gualmini/FinalAssignment/main/owid-co2-data.csv"
CO2_df = pd.read_csv(url)
CO2_df.dropna(subset=["iso_code"], inplace=True)
CO2_backup_df = CO2_df.copy()

# ===C02 emissions and GDP ====

CO2_df.dropna(subset=["co2", "gdp"], inplace=True)
corr, p_value = pearsonr(CO2_df["co2"], CO2_df["gdp"])


print(f"Pearson correlation coefficient bewteen total C02 emissions and total GDP: {corr}. P-value: {p_value}")

CO2_df["CO2 per capita"] = CO2_df["co2"] / CO2_df["population"]
CO2_df["GDP per capita"] = CO2_df["gdp"] / CO2_df["population"]
CO2_df.dropna(subset=["CO2 per capita", "GDP per capita"], inplace=True)
corr, p_value = pearsonr(CO2_df["CO2 per capita"], CO2_df["GDP per capita"])

print(f"Pearson correlation coefficient between CO2 emissions per capita and GDP per capita: {corr}. P-value: {p_value}")

# Create scatter plot with regression line
plt.scatter(CO2_df["co2"], CO2_df["gdp"])
slope, intercept, _, _, _ = linregress(CO2_df["co2"], CO2_df["gdp"])
regression_line = intercept + slope * CO2_df["co2"]
plt.plot(CO2_df["co2"], regression_line, color='red')
plt.xlabel("CO2 Emissions")
plt.ylabel("GDP")
plt.title("CO2 Emissions vs. GDP")
plt.show()

# Create scatter plot for per capita data with regression line
plt.scatter(CO2_df["CO2 per capita"], CO2_df["GDP per capita"])
slope, intercept, _, _, _ = linregress(CO2_df["CO2 per capita"], CO2_df["GDP per capita"])
regression_line = intercept + slope * CO2_df["CO2 per capita"]
plt.plot(CO2_df["CO2 per capita"], regression_line, color='red')
plt.xlabel("CO2 Emissions per capita")
plt.ylabel("GDP per capita")
plt.title("CO2 Emissions per capita vs. GDP per capita")
plt.show()

# ===C02 emissions and diet ====

# first we take the relevant data from teh CO2 database
CO2_and_diet_df = CO2_backup_df.loc[:, ["country", "year", "co2", "population"]]
CO2_and_diet_df.dropna(subset=["co2"], inplace=True)
CO2_and_diet_df["CO2 per capita"] = CO2_and_diet_df["co2"] / CO2_and_diet_df["population"]

#then we add data about diet
url = "https://raw.githubusercontent.com/gualmini/FinalAssignment/main/dietary-compositions-by-commodity-group.csv"
diet_df = pd.read_csv(url)
diet_df["Total intake in Kilocalories"] = diet_df.iloc[:, 3:13].sum(axis=1)

# Calculate the percentage of calories for each dietary group and we add it to the CO2_and_diet_df
for col in diet_df.columns[3:]:
    commodity = col.split(" ")[0]  # Extract the first word from the column label
    CO2_and_diet_df[f"% of calories from {commodity}"] = (diet_df[col] / diet_df["Total intake in Kilocalories"]) * 100

# Select the columns for correlation calculation
correlation_columns = CO2_and_diet_df.columns[5:-1]

# Calculate the correlations and p-values
correlations = {}
p_values = {}

for column in correlation_columns:
    non_empty_rows = CO2_and_diet_df.dropna(subset=["CO2 per capita", column])

    x = non_empty_rows["CO2 per capita"]
    y = non_empty_rows[column]

    # Calculate the correlation and p-value using scipy.stats.pearsonr
    corr, p_value = pearsonr(x, y)
    correlations[column] = corr
    p_values[column] = p_value

# Create a correlation matrix dataframe
correlation_matrix = pd.DataFrame({"Correlation": correlations, "P-value": p_values})

# Add direction values
correlation_matrix["Direction"] = ["Positive" if c > 0 else "Negative" for c in correlation_matrix["Correlation"]]


# Add significance notation based on p-values
significance_levels = {
    (0.0, 0.0001): "***",
    (0.0001, 0.001): "**",
    (0.001, 0.01): "*",
    (0.01, 0.05): "Marginally significant",
    (0.05, float("inf")): "Non-Significant"
}

correlation_matrix["Significance"] = [
    next(sign for (start, end), sign in significance_levels.items() if start < p <= end)
    for p in correlation_matrix["P-value"]
]

# Reorder the columns
correlation_matrix = correlation_matrix[["Correlation", "Direction", "P-value", "Significance"]]

print(correlation_matrix)





