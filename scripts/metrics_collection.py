import csv
import subprocess
import pandas as pd

# Define paths and filenames
REPO_PATH = "hive"
CSV_INPUT_FILE = "processed_data/attempt_2/filtered_hive_tags_commits.csv"
CSV_OUTPUT_FILE = "processed_data/attempt_2/metrics_output.csv"
UND_PROJECT_FILE = "my_project.udb"  # Path to the manually created Understand project file

# Define the list of metrics to retrieve from Understand
METRICS = [
    "Kind", "Name", "AvgCountLine", "AvgCountLineBlank", "AvgCountLineCode", "AvgCountLineComment", 
    "AvgCyclomatic", "CountClassBase", "CountClassCoupled", "CountClassCoupledModified", 
    "CountClassDerived", "CountDeclClass", "CountDeclClassMethod", "CountDeclClassVariable", 
    "CountDeclExecutableUnit", "CountDeclFile", "CountDeclFunction", "CountDeclInstanceMethod", 
    "CountDeclInstanceVariable", "CountDeclMethod", "CountDeclMethodAll", "CountDeclMethodDefault", 
    "CountDeclMethodPrivate", "CountDeclMethodProtected", "CountDeclMethodPublic", "CountInput", 
    "CountLine", "CountLineBlank", "CountLineCode", "CountLineCodeDecl", "CountLineCodeExe", 
    "CountLineComment", "CountOutput", "CountSemicolon", "CountStmt", "CountStmtDecl", 
    "CountStmtExe", "Cyclomatic", "MaxCyclomatic", "MaxInheritanceTree", "MaxNesting", 
    "PercentLackOfCohesion", "PercentLackOfCohesionModified", "RatioCommentToCode", "SumCyclomatic", 
    "CountDeclFileCode", "CountDeclFileHeader", "CountDeclInstanceVariablePrivate", 
    "CountDeclInstanceVariableProtected", "CountDeclInstanceVariablePublic", "CountDeclMethodConst", 
    "CountDeclMethodFriend", "CountLineInactive", "CountLinePreprocessor", "CountStmtEmpty"
]

def checkout_commit(repo_path, commit_hash):
    """Check out a specific commit in the Git repository."""
    subprocess.run(["git", "checkout", commit_hash], cwd=repo_path, check=True)

def analyze_existing_project():
    """Reanalyze the existing Understand project after checking out a new commit."""
    subprocess.run(["und", "analyze", "-db", UND_PROJECT_FILE], check=True)

def get_metrics():
    """Retrieve metrics from Understand and return them as a list of dictionaries."""
    metrics_data = []
    command = ["und", "metrics", "-db", UND_PROJECT_FILE, "-all"]
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Process each line of output as a CSV row
    reader = csv.DictReader(result.stdout.splitlines())
    for row in reader:
        metrics_data.append(row)
    return metrics_data

def main():
    # Read the input CSV file with version tags and commit hashes
    versions = pd.read_csv(CSV_INPUT_FILE)

    # Prepare the output CSV file
    with open(CSV_OUTPUT_FILE, mode='w', newline='') as output_file:
        writer = csv.writer(output_file)
        # Write the header row
        header = ["Version", "CommitId", "File"] + METRICS
        writer.writerow(header)

        # Process each version/commit
        for index, row in versions.iterrows():
            version = row["Tag"]
            commit_id = row["Commit Hash"]

            print(f"Processing version {version} with commit {commit_id}...")

            # Checkout the specified commit
            checkout_commit(REPO_PATH, commit_id)

            # Reanalyze the existing Understand project to update metrics
            analyze_existing_project()
            metrics_data = get_metrics()

            # Write each file's metrics to the CSV output
            for file_metrics in metrics_data:
                row_data = [version, commit_id, file_metrics["Name"]] + [file_metrics.get(metric, "") for metric in METRICS]
                writer.writerow(row_data)

    # Clean up by checking out the main branch again
    subprocess.run(["git", "checkout", "main"], cwd=REPO_PATH, check=True)
    print(f"Metrics collection completed and saved to {CSV_OUTPUT_FILE}")

if __name__ == "__main__":
    main()
