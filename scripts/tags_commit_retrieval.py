import subprocess
import csv

# Path to your cloned repository
repo_path = 'hive_repo/hive'  # replace with the path to your local repository

# Output CSV file path
output_csv = 'processed_data/attempt_2/git_tags.csv'

# Function to get all tags and their associated commit hashes
def get_git_tags():
    try:
        # Run the git command to list tags with their commit hashes
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

# Export tags to CSV
def export_tags_to_csv(tags, csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Commit Hash', 'Tag Name'])  # Header row
        writer.writerows(tags)  # Write tag data

    print(f"Tags exported to {csv_file}")

# Get tags and export to CSV
tags = get_git_tags()
if tags:
    export_tags_to_csv(tags, output_csv)
