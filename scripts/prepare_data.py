import pandas as pd
import os

# Step 1: Define the folder containing the CSV files
input_folder = 'processed_data/attempt_2/split_by_version'  # Adjust the folder path as necessary
output_folder = 'processed_data/attempt_2/split_by_version_clean'  # Folder to save the cleaned files

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Step 2: Loop through all CSV files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):  # Process only CSV files
        # Full file path
        input_file_path = os.path.join(input_folder, filename)
        
        # Step 3: Load the dataset
        data = pd.read_csv(input_file_path)
        
        # Step 4: Drop the unnecessary columns
        data_cleaned = data.drop(columns=['Version', 'CommitId', 'Fichier'])

        # Step 5: Save the cleaned dataset to the output folder
        output_file_path = os.path.join(output_folder, f"cleaned_{filename}")
        data_cleaned.to_csv(output_file_path, index=False)
        
        print(f"Processed and saved cleaned file: {output_file_path}")
