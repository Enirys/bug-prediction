import pandas as pd
import os

# Load the first CSV with bug data
bugs_df = pd.read_csv('processed_data/attempt_2/filtered_java_cpp_files.csv')  # Replace 'bugs.csv' with your actual file path
# Load the second CSV with metrics data
metrics_df = pd.read_csv('processed_data/attempt_2/metrics_all_versions_cleaned.csv', delimiter=';')  # Replace 'metrics.csv' with your actual file path

# Rename columns for consistency
bugs_df = bugs_df.rename(columns={'Affected Version': 'Version', 'File': 'Fichier'})
metrics_df = metrics_df.rename(columns={'Version': 'Version', 'Fichier': 'Fichier'})

# Extract the file name from the full path in the bugs data
bugs_df['Fichier'] = bugs_df['Fichier'].apply(lambda x: os.path.basename(x))

# Merge data by checking if each file and version in the metrics file is a bug
merged_df = metrics_df.merge(bugs_df[['Bug ID', 'Fichier', 'Version']], 
                             on=['Fichier', 'Version'], 
                             how='left', 
                             indicator='is_bug')

# Add 'is_bug' column where '1' means it matches a bug, and '0' means no bug
merged_df['is_bug'] = merged_df['is_bug'].apply(lambda x: 1 if x == 'both' else 0)

# Optional: Drop 'Bug ID' column if it's not needed in the final output
merged_df = merged_df.drop(columns=['Bug ID'])

# Save the result to a new CSV
merged_df.to_csv('processed_data/attempt_2/metrics_with_is_bug.csv', index=False)

# Display example output
print(merged_df.head())
