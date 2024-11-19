import pandas as pd

# Load the CSV file
input_csv = "processed_data/attempt_2/cleaned_file.csv"  # The CSV file with metrics data
output_csv = "processed_data/attempt_2/metrics_all_versions_cleaned.csv"  # Output CSV file after cleaning

# Load the data
df = pd.read_csv(input_csv)

# Print initial summary of missing values
print("Initial missing values per column:\n", df.isnull().sum())

# Step 1: Drop columns with any missing values
df = df.dropna(axis=1, how='any')

# Step 2: Drop any rows that are completely empty (all NaN values)
df = df.dropna(how='all')

# Print summary after removing columns and empty rows
print("Columns remaining after dropping columns with missing values:\n", df.columns)
print("Number of rows after removing completely empty rows:", len(df))
print("Missing values after cleaning:\n", df.isnull().sum())

# Save the cleaned data to a new CSV file
df.to_csv(output_csv, index=False)
print(f"Cleaned data saved to {output_csv}")
