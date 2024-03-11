import pandas as pd
import glob
import os

# Function to calculate and return summary statistics for a DataFrame
def calculate_summary_stats(df, label_suffix):
    if df.empty:
        return pd.DataFrame()
    numerical_cols = ['AVG', 'MIN', 'MAX', 'MEDIAN']
    df[numerical_cols] = df[numerical_cols].astype(float)
    summaries = pd.DataFrame({
        'File': [f'AVERAGES ({label_suffix})', f'MINIMUM ({label_suffix})', f'MAXIMUM ({label_suffix})'],
        'AVG': [df['AVG'].mean(), df['AVG'].min(), df['AVG'].max()],
        'MIN': [df['MIN'].mean(), df['MIN'].min(), df['MIN'].max()],
        'MAX': [df['MAX'].mean(), df['MAX'].min(), df['MAX'].max()],
        'MEDIAN': [df['MEDIAN'].mean(), df['MEDIAN'].min(), df['MEDIAN'].max()]
    })
    return summaries

# Initialize empty DataFrames for accumulating results
results_metal = []
results_no_metal = []

# Sort files asciibetically and process
for file_path in sorted(glob.glob('portfolio_value_*.csv')):
    filename = os.path.basename(file_path)
    df = pd.read_csv(file_path, usecols=['TOTALS'])
    
    # Prepare statistics
    statistics = {
        'File': filename,
        'AVG': df['TOTALS'].mean(),
        'MIN': df['TOTALS'].min(),
        'MAX': df['TOTALS'].max(),
        'MEDIAN': df['TOTALS'].median()
    }
    
    # Append to the appropriate list
    if 'nometals' in filename:
        results_no_metal.append(statistics)
    else:
        results_metal.append(statistics)

# Convert lists to DataFrames
df_metal = pd.DataFrame(results_metal)
df_no_metal = pd.DataFrame(results_no_metal)

# Calculate and append summary statistics
summary_metal = calculate_summary_stats(df_metal, 'metals')
summary_no_metal = calculate_summary_stats(df_no_metal, 'no-metals')

# Concatenate results and summaries
final_df = pd.concat([df_metal, df_no_metal, summary_metal, summary_no_metal], ignore_index=True)

# Setting float format for pandas
pd.set_option('display.float_format', '{:.2f}'.format)

# Print the final DataFrame
print(final_df.to_string(index=False))

