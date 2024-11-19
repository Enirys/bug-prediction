import subprocess
import pandas as pd
import glob

# Directory containing the CSV files
csv_files_path = 'raw_data/all_fields_data_new/*.csv'

# List to store individual DataFrames
dataframes = []

# Read each CSV file and keep only necessary columns
for file in glob.glob(csv_files_path):
    df = pd.read_csv(file)

    # Extract bug-related data by selecting relevant columns
    base_columns = ['Issue key']  # Basic columns we want to keep
    affected_version_columns = [col for col in df.columns if col.startswith("Affects Version/s")]
    fix_version_columns = [col for col in df.columns if col.startswith("Fix Version/s")]
    
    # Create a DataFrame containing only relevant columns
    relevant_df = df[base_columns + affected_version_columns + fix_version_columns].copy()
    
    # Rename columns for clarity
    relevant_df = relevant_df.rename(columns={'Issue key': 'Bug ID'})
    
    # Append the DataFrame to the list
    dataframes.append(relevant_df)

# Combine all DataFrames into one
combined_bugs_df = pd.concat(dataframes, ignore_index=True)

# Prepare a list to store associations between bugs and files
bug_file_associations = []

# Loop over each bug to search for it in the Git log
for _, row in combined_bugs_df.iterrows():
    bug_id = row['Bug ID']
    
    # Gather affected and fix versions, ignoring NaN values
    affected_versions = [row[col] for col in affected_version_columns if pd.notna(row[col])]
    fix_versions = [row[col] for col in fix_version_columns if pd.notna(row[col])]
    
    # Use `git log` to find commits mentioning the bug ID in commit messages
    try:
        git_log_cmd = f"git -C hive_repo/hive log --all --grep=\"{bug_id}\" --pretty=format:\"%H\""
        commit_hashes = subprocess.check_output(git_log_cmd, shell=True).decode().splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error finding commits for Bug ID {bug_id}: {e}")
        continue
    
    # For each commit found, get the list of modified files
    for commit_hash in commit_hashes:
        git_show_cmd = f"git -C hive_repo/hive show --pretty=\"\" --name-only {commit_hash}"
        modified_files = subprocess.check_output(git_show_cmd, shell=True).decode().splitlines()
        
        # For each affected version, add modified files to the association list
        for affected_version in affected_versions:
            for file_path in modified_files:
                bug_file_associations.append({
                    'Bug ID': bug_id,
                    'File': file_path,
                    'Affected Version': affected_version,
                    'Fix Versions': ", ".join(fix_versions)  # Keep fix versions as a comma-separated string
                })

# Convert results to DataFrame and save as CSV
bug_file_df = pd.DataFrame(bug_file_associations)
bug_file_df.to_csv('processed_data/attempt_2/bug_file_associations.csv', index=False)
