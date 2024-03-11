import pandas as pd
import sys
from datetime import datetime

# Read historical data
def read_historical_data():
    return pd.read_csv('historical_currency_values.csv', index_col='Date', parse_dates=True)

# Find the nearest valid date for the start date
def get_valid_start_date(historical_data, start_date):
    for i in range(14):  # Look up to 14 days ahead if the exact date is unavailable
        try_date = pd.Timestamp(start_date) + pd.Timedelta(days=i)
        if try_date.strftime('%Y-%m-%d') in historical_data.index:
            return try_date.strftime('%Y-%m-%d')
    return None

def process_results(filtered_data, results, valid_start_date, file_prefix):
        # Convert results to DataFrame and use valid start date for index
        results_df = pd.DataFrame(results, index=filtered_data.index)

        # Filter out any rows containing a blank field or an 'X':
        results_df.replace('X', pd.NA, inplace=True)  # Optional: Convert 'X' to NaN for uniform handling
        results_df.dropna(inplace=True)  # Drop all rows with any NaN values


        num_currencies = len(basket)
        # Calculate totals directly and round to 2 decimal places
        results_df['TOTALS'] = results_df.iloc[:, :num_currencies].replace('X', 0).sum(axis=1).round(2)

        
        output_file_name = f"{file_prefix}{pd.Timestamp(valid_start_date).strftime('%Y%m%d')}.csv"
        results_df.to_csv(output_file_name)
        print(f"Portfolio value simulation saved to {output_file_name}")

# Simulate the portfolio for each start date
def simulate_portfolio(start_dates, basket, historical_data):
    metals = ['Gold', 'Silver', 'Platinum', 'Palladium']  # Define metals to be excluded
    for start_date in start_dates:
        valid_start_date = get_valid_start_date(historical_data, start_date)
        if not valid_start_date:
            print(f"No valid data for {start_date}, skipping simulation.")
            continue
        
        # Adjust the historical data to start from the valid start date
        filtered_data = historical_data.loc[valid_start_date:]
        
        results = {}
        results_nometals = {}

        # Calculate total investment excluding metals
        total_excluding_metals = sum(amount for currency, amount in basket.items() if currency not in metals)

        # Adjust investment amounts for non-metal currencies
        adjusted_basket = {currency: amount * (sum(basket.values()) / total_excluding_metals)
                           for currency, amount in basket.items() if currency not in metals}

        for currency, amount in basket.items():
            if currency in filtered_data.columns:
                # Attempt to find the first non-NA rate in rows 0 to 13, i.e. first 2 weeks of data
                initial_rate = None
                for row in range(14):  # Look through rows 0 to 13 - first 2 weeks of data
                    rate = filtered_data.iloc[row].get(currency, pd.NA)
                    if not pd.isna(rate):
                        initial_rate = rate
                        break

                if initial_rate is None:  # Check if no valid initial rate was found
                    results[currency] = pd.Series(['X'] * len(filtered_data), index=filtered_data.index)
                    if currency in adjusted_basket:  # Also update the nometals results if applicable
                        results_nometals[currency] = pd.Series(['X'] * len(filtered_data), index=filtered_data.index)
                    continue

                initial_units = amount / initial_rate
                # Track value over time from the valid start date
                results[currency] = filtered_data[currency] * initial_units
                if currency in adjusted_basket:  # Calculate for adjusted basket
                    adjusted_amount = adjusted_basket[currency]
                    adjusted_units = adjusted_amount / initial_rate
                    results_nometals[currency] = filtered_data[currency] * adjusted_units
            else:
                # If currency data is missing, fill the column with 'X'
                results[currency] = pd.Series(['X'] * len(filtered_data), index=filtered_data.index)
                if currency in adjusted_basket:
                    results_nometals[currency] = pd.Series(['X'] * len(filtered_data), index=filtered_data.index)

        # Process results for the original portfolio
        process_results(filtered_data, results, valid_start_date, "portfolio_value_")
        # Process results for the adjusted (nometals) portfolio
        process_results(filtered_data, results_nometals, valid_start_date, "portfolio_value_nometals_")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 basket-simulator.py <input_file_name>")
        sys.exit(1)

    input_file_name = sys.argv[1]
    basket = pd.read_csv(input_file_name, sep=':', names=['Currency', 'Amount'], skipinitialspace=True)
    basket['Amount'] = basket['Amount'].str.replace('k', '').astype(float) * 1000
    basket = dict(zip(basket.Currency, basket.Amount))

    historical_data = read_historical_data()

    start_dates = [
        '2010-01-01', '2010-06-01', '2015-01-01', '2015-06-01',
        '2020-01-01', '2020-06-01', '2021-01-01', '2021-06-01',
        '2022-01-01', '2022-06-01', '2023-01-01', '2023-06-01', '2024-01-01'
    ]

    simulate_portfolio(start_dates, basket, historical_data)

