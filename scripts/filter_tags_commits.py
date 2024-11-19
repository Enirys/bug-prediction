import pandas as pd
import subprocess
import csv

# Paths to the local repository and CSV files
repo_path = 'hive_repo/hive'  # replace with the path to your cloned repository
versions_csv = 'processed_data/attempt_2/filtered_java_cpp_files.csv'  # replace with the path to your CSV file
output_csv = 'processed_data/attempt_2/filtered_git_tags.csv'

# Step 1: Load the required versions from the CSV file
data = pd.read_csv(versions_csv)
required_versions = set(data['Affected Version'].dropna().str.strip())

# Step 2: Get all tags and their commit hashes from the Git repository
def get_git_tags():
    try:
        tags = subprocess.check_output(
            ['git', 'show-ref', '--tags'],
            cwd=repo_path
        ).decode('utf-8').strip().splitlines()
        
        # Process the output into a list of tuples (commit hash, tag name)
        tag_list = [(line.split()[0], line.split()[1].replace('refs/tags/', '')) for line in tags]
        return tag_list
    except subprocess.CalledProcessError as e:
        print(f"Error fetching tags: {e}")
        return []

# Step 3: Filter tags to only include those that contain any of the required versions as a substring
def filter_tags(tags, versions):
    filtered_tags = [tag for tag in tags if any(version in tag[1] for version in versions)]
    return filtered_tags

# Step 4: Export filtered tags to a CSV file
def export_tags_to_csv(tags, csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Commit Hash', 'Tag Name'])  # Header row
        writer.writerows(tags)  # Write tag data

    print(f"Filtered tags exported to {csv_file}")

# Execute the steps
tags = get_git_tags()
filtered_tags = filter_tags(tags, required_versions)
if filtered_tags:
    export_tags_to_csv(filtered_tags, output_csv)
else:
    print("No matching tags found for the specified versions.")
