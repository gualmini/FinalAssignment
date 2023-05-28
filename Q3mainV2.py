import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Read the CSV file from the GitHub URL and create the DataFrame
url = "https://raw.githubusercontent.com/gualmini/FinalAssignment/main/levelized-cost-of-energy.csv"
levelized_cost_of_energy_df = pd.read_csv(url)

# Prompt user for the country of interest
country = input("What country are you interested in? ").capitalize()

# Check if the country is in the DataFrame
if country in levelized_cost_of_energy_df["Entity"].values:
    entity_under_consideration = country
else:
    print("We do not have data for the country you selected, so we will show you data for the whole world.")
    entity_under_consideration = "World"

# Filter the DataFrame for the entity under consideration
entity_data = levelized_cost_of_energy_df[levelized_cost_of_energy_df["Entity"] == entity_under_consideration]

# Figure 1: Scatter plot of actual prices
plt.figure(1)
for column in entity_data.columns[3:]:
    plt.scatter(entity_data["Year"], entity_data[column], label=column)

plt.xlabel("Year")
plt.ylabel("Price")
plt.title("Actual Prices of Levelized Cost of Energy ({})".format(entity_under_consideration))
plt.legend()
plt.xticks(rotation=45)
plt.xlim(left=entity_data["Year"].min() - 2)
plt.ylim(bottom=0)

plt.show()

# Dictionary to store regression line equations
regression_equations = {}

# Figures 2 onwards: Regression lines
for column in entity_data.columns[3:]:
    plt.figure()
    x = entity_data["Year"]
    y = entity_data[column]

    # Skip the column if it does not contain any digits
    if any(isinstance(value, (int, float)) for value in y) and y.notna().any():
        # Filter out missing values from x and y
        valid_indices = x.notna() & y.notna()
        x_valid = x[valid_indices]
        y_valid = y[valid_indices]

        # Calculate regression parameters for the non-missing data
        slope, intercept, _, _, _ = linregress(x_valid, y_valid)
        regression_line = intercept + slope * x_valid

        # Store regression line equation
        regression_equations[column] = [slope, intercept]

        # Plot the scatter plot of actual prices
        plt.scatter(x_valid, y_valid, label="Actual Prices ({})".format(column))

        # Plot the regression line
        plt.plot(x_valid, regression_line, color='red', label="Regression Line ({})".format(column))

        plt.xlabel("Year")
        plt.ylabel("Price")
        plt.title("Regression Line for {} ({})".format(column, entity_under_consideration))
        plt.legend()

    plt.show()

# Prompt the user for the year
valid_input = False
while not valid_input:
    user_input = input("For what year would you like to know the prices based on the current trend? ")

    if user_input.isdigit():
        input_year = int(user_input)
        valid_input = True
    else:
        print("Invalid input. Please enter a valid year.")

# calculate and print predicted price
for energy_source in regression_equations.keys():
    slope, intercept = regression_equations[energy_source]
    predicted_price = slope * input_year + intercept
    if predicted_price <= 0:
        print(f"Based on current trends, in {input_year} {energy_source} will be virtually zero")
    else:
        print(f"Based on current trends, {energy_source} in {input_year} will be {predicted_price}")
