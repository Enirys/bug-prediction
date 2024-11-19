import csv
import subprocess
import os

def get_last_commit(version):
    """Get the last commit for the specified version."""
    try:
        # Run the git command to get the last commit for the specified version
        commit_hash = subprocess.check_output(
            ['git', 'rev-list', '-n', '1', 'tags/{}'.format(version)],
            stderr=subprocess.STDOUT
        ).strip().decode('utf-8')
        return commit_hash
    except subprocess.CalledProcessError as e:
        print(f"Error finding commit for version {version}: {e.output.decode()}")
        return None

def checkout_commit(commit_hash):
    """Checkout the specified commit."""
    try:
        subprocess.run(['git', 'checkout', commit_hash], check=True)
        print(f"Checked out commit: {commit_hash}")
    except subprocess.CalledProcessError as e:
        print(f"Error checking out commit {commit_hash}: {e.output.decode()}")

def get_changed_files(commit_hash):
    """Get the list of changed files for the specified commit."""
    try:
        changed_files = subprocess.check_output(
            ['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', commit_hash],
            stderr=subprocess.STDOUT
        ).strip().decode('utf-8').split('\n')
        return changed_files
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving changed files for commit {commit_hash}: {e.output.decode()}")
        return []

def main(csv_file, output_file):
    # Create or overwrite the output CSV file
    with open(output_file, mode='w', newline='') as outfile:
        fieldnames = ['Affected Version', 'Commit ID', 'Changed Files']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Read the versions from the CSV file
        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                version = row['Affected Version']
                print(f"Processing version: {version}")
                commit_hash = get_last_commit(version)
                if commit_hash:
                    checkout_commit(commit_hash)
                    changed_files = get_changed_files(commit_hash)
                    # Write the results to the output file
                    for file in changed_files:
                        writer.writerow({
                            'Affected Version': version,
                            'Commit ID': commit_hash,
                            'Changed Files': file
                        })
                    print(f"Recorded changed files for version {version}")
                else:
                    print(f"No commit found for version {version}")
                print()  # Add a new line for better readability
    print(f"CSV report generated successfully at {output_file}")

if __name__ == "__main__":
    # Ensure the script is run in the correct directory (where the Git repo is located)
    os.chdir('hive_repo/hive')  # Change this to your Hive repo path
    main('processed_data/attempt_2/filtered_java_cpp_files.csv', 'processed_data/attempt_2/changed_files_last_commit_report.csv')
