import pandas as pd
import glob
import os

# Pattern to match all 'portfolio_value_*.csv' files
file_pattern = 'portfolio_value_*.csv'
files = sorted(glob.glob(file_pattern))  # Sort files asciibetically

# Initialize an empty DataFrame for the results
results = pd.DataFrame()

for file_path in files:
    # Extract the filename for display purposes
    filename = os.path.basename(file_path)
    
    # Read the CSV file, focusing on the 'TOTALS' column
    df = pd.read_csv(file_path, usecols=['TOTALS'])
    
    # Calculate statistics and format to avoid scientific notation
    avg = '{:.2f}'.format(df['TOTALS'].mean())
    min_val = '{:.2f}'.format(df['TOTALS'].min())
    max_val = '{:.2f}'.format(df['TOTALS'].max())
    median_val = '{:.2f}'.format(df['TOTALS'].median())
    
    # Append the results
    new_row = pd.DataFrame([{'File': filename, 'AVG': avg, 'MIN': min_val, 'MAX': max_val, 'MEDIAN': median_val}])
    results = pd.concat([results, new_row], ignore_index=True)

# Convert numerical columns back to floats for aggregation
numerical_cols = ['AVG', 'MIN', 'MAX', 'MEDIAN']
results[numerical_cols] = results[numerical_cols].astype(float)

# Append AVERAGES, MINIMUM, and MAXIMUM rows
results = pd.concat([
    results,
    pd.DataFrame([results[numerical_cols].mean()], index=['AVERAGES']).assign(File='AVERAGES'),
    pd.DataFrame([results[numerical_cols].min()], index=['MINIMUM']).assign(File='MINIMUM'),
    pd.DataFrame([results[numerical_cols].max()], index=['MAXIMUM']).assign(File='MAXIMUM')
], ignore_index=True)

# Ensure numbers are displayed as raw numbers
pd.options.display.float_format = '{:.2f}'.format

# Print the results
print(results.to_string(index=False))

