import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

brent_prices_df = pd.read_csv("brent.csv")
brent_prices_df.dropna(inplace=True)

brent_prices_df["Date"] = pd.to_datetime(brent_prices_df["Date"], format="%b %d, %Y")


# plotting the price over time
brent_prices_df.plot(x="Date", y="Price")
plt.xlabel("Date")
plt.ylabel("Brent Oil Price")
plt.legend().remove()
plt.show()


#linear regression part
x = brent_prices_df["Date"].astype("int64") // 10**9  # Convert datetime to seconds
y = brent_prices_df["Price"]
slope, intercept, r_value, p_value, std_err = linregress(x, y)

print(f"It looks like we can express the price across time with the following equation: Brent Oil price = {slope:.2f}time^ + {intercept:.2f}")
print(f"^ time calculated as seconds since January 1st, 1970")

#ask user for a date in the future and give predicted price
def predict_price(date_str):
    date = pd.to_datetime(date_str, format="%d-%m-%Y")
    seconds_since_epoch = int(date.timestamp())

    latest_date = brent_prices_df["Date"].max()
    if date <= latest_date:
        latest_price = brent_prices_df[brent_prices_df["Date"] == latest_date]["Price"].iloc[0]
        print(
            f"Data is available for {date_str}. The price on that day was {latest_price:.2f}.")
        return None

    predicted_price = slope * seconds_since_epoch + intercept
    return predicted_price

date_str = input("Enter a date in the future (format: day-month-year, with year as four digits) to know the predicted Brent Oil price: ")
predicted_price = predict_price(date_str)

if predicted_price is not None:
    print(f"The predicted price for Brent oil on {date_str} is {predicted_price:.2f}")
