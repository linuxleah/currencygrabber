import pandas as pd
import glob
import os

# Pattern to match all 'portfolio_value_*.csv' files
file_pattern = 'portfolio_value_*.csv'
files = sorted(glob.glob(file_pattern))  # Sort files asciibetically

# Initialize two empty DataFrames for the results
results_metal = pd.DataFrame()
results_no_metal = pd.DataFrame()

for file_path in files:
    # Extract the filename for display purposes
    filename = os.path.basename(file_path)
    
    # Determine if the file is a metals or no-metals file
    is_no_metal = 'nometals' in filename
    
    # Read the CSV file, focusing on the 'TOTALS' column
    df = pd.read_csv(file_path, usecols=['TOTALS'])
    
    # Calculate statistics and format to avoid scientific notation
    statistics = {
        'File': filename, 
        'AVG': '{:.2f}'.format(df['TOTALS'].mean()), 
        'MIN': '{:.2f}'.format(df['TOTALS'].min()), 
        'MAX': '{:.2f}'.format(df['TOTALS'].max()), 
        'MEDIAN': '{:.2f}'.format(df['TOTALS'].median())
    }
    
    # Append the results to the appropriate DataFrame
    if is_no_metal:
        results_no_metal = pd.concat([results_no_metal, pd.DataFrame([statistics])], ignore_index=True)
    else:
        results_metal = pd.concat([results_metal, pd.DataFrame([statistics])], ignore_index=True)

# Function to append AVG, MIN, MAX to results DataFrame
def append_summary_stats(results_df, label_suffix):
    if not results_df.empty:
        numerical_cols = ['AVG', 'MIN', 'MAX', 'MEDIAN']
        results_df[numerical_cols] = results_df[numerical_cols].astype(float)
        summary_rows = pd.concat([
            pd.DataFrame([results_df[numerical_cols].mean()], index=['AVERAGES']).assign(File=f'AVERAGES ({label_suffix})'),
            pd.DataFrame([results_df[numerical_cols].min()], index=['MINIMUM']).assign(File=f'MINIMUM ({label_suffix})'),
            pd.DataFrame([results_df[numerical_cols].max()], index=['MAXIMUM']).assign(File=f'MAXIMUM ({label_suffix})')
        ])
        return pd.concat([results_df, summary_rows], ignore_index=True)
    return results_df

# Append summary statistics
results_metal = append_summary_stats(results_metal, 'metals')
results_no_metal = append_summary_stats(results_no_metal, 'no-metals')

# Combine both DataFrames and sort by filename to ensure summaries appear at the bottom
results_combined = pd.concat([results_metal, results_no_metal], ignore_index=True).sort_values(by='File', key=lambda x: x.str.lower())

# Ensure numbers are displayed as raw numbers
pd.options.display.float_format = '{:.2f}'.format

# Print the results
print(results_combined.to_string(index=False))

