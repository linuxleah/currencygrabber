import sys
import yfinance as yf
import pandas as pd
import time

# Configuration
sleep_after_every_n = 5  # Customize this to your needs
sleep_duration = 10      # Customize this to your needs (in seconds)

def read_input_data(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return data

def construct_symbol(currency):
    if currency == "Gold":
        return "GC=F"
    else:
        return f"{currency}USD=X"

def fetch_and_save_data(input_data, output_csv_path):
    # Parse input data
    currencies = {}
    for line in input_data.strip().split('\n'):
        currency, amount = line.split(':')
        currency = currency.strip()
        currencies[currency] = 1

    # Prepare for data fetching
    start_date = "2010-01-01"
    end_date = pd.Timestamp.today().strftime('%Y-%m-%d')  # Today's date

    # Fetch historical data
    all_data = []
    for i, (currency, amount) in enumerate(currencies.items(), 1):
        symbol = construct_symbol(currency)

        data = yf.download(symbol, start=start_date, end=end_date)
        data['Value'] = data['Close'] * amount  # Calculate value in USD
        data = data[['Value']]  # Keep only the 'Value' column
        data = data.copy()
        data.rename(columns={'Value': currency}, inplace=True)
        data.columns = [currency]  # Ensure the column is named only after the currency
        all_data.append(data)


        # Sleep to avoid rate-limiting
        if i % sleep_after_every_n == 0:
            time.sleep(sleep_duration)

    # Combine all data into a single DataFrame
    combined_data = pd.concat(all_data, axis=1)
    combined_data.index.name = 'Date'

    # Write to CSV
    combined_data.to_csv(output_csv_path)
    print(f"Data written to {output_csv_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 currency-grabber.py <input_file_name>")
        sys.exit(1)

    input_file_name = sys.argv[1]
    output_csv_path = "historical_currency_values.csv"
    
    input_data = read_input_data(input_file_name)
    fetch_and_save_data(input_data, output_csv_path)

