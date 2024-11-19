import pandas as pd
import os

# Step 1: Define the folder containing the CSV file
input_file_path = 'processed_data/attempt_2/metrics_with_is_bug.csv'  # Adjust path as needed
output_folder = 'processed_data/attempt_2/split_by_version/'  # Folder to save the separate CSV files

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Step 2: Load the dataset
data = pd.read_csv(input_file_path)

# Step 3: Convert the 'Version' column to a string and ensure Patch version is 0
# Convert version to string with format Major.Minor.Patch (e.g., 2.0.0 from 2.0)
data['Version'] = data['Version'].apply(lambda x: f"{int(x)}.0.0" if len(str(x).split('.')) == 2 else str(x))

# Step 4: Filter versions that have patch version as 0
# We will split the version by '.' and keep rows where the third part (Patch) is 0
data_filtered = data[data['Version'].apply(lambda x: len(x.split('.')) == 3 and x.split('.')[2] == '0')]

# Step 5: Loop through each unique version and save as separate CSV files
for version, group in data_filtered.groupby('Version'):
    # Define the file path for each version
    output_file_path = os.path.join(output_folder, f"{version}.csv")
    
    # Save the group (version) data to a new CSV file
    group.to_csv(output_file_path, index=False)
    
    print(f"File for version {version} saved as {output_file_path}")
