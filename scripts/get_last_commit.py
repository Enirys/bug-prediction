import requests
import csv
from dotenv import load_dotenv
import os

# Load the GitHub token from the .env file
load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def get_all_tags(owner, repo):
    tags = []
    page = 1
    while True:
        url = f'https://api.github.com/repos/{owner}/{repo}/tags?page={page}&per_page=100'
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code != 200:
            print(f"Error: Unable to fetch tags (status code: {response.status_code})")
            break
        
        page_tags = response.json()
        
        # If no more tags are returned, break the loop
        if not page_tags:
            break

        tags.extend(page_tags)
        page += 1

    return tags

def get_commit_of_tag(owner, repo, tag):
    # Fetch reference for the tag
    url = f'https://api.github.com/repos/{owner}/{repo}/git/refs/tags/{tag}'
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error: Unable to fetch commit for tag {tag} (status code: {response.status_code})")
        return None

    tag_info = response.json()
    # Check if the tag points to a tag object or a commit
    if tag_info['object']['type'] == 'commit':
        return tag_info['object']['sha']
    elif tag_info['object']['type'] == 'tag':
        # If it's an annotated tag, follow the tag object to get the commit
        tag_url = tag_info['object']['url']
        tag_response = requests.get(tag_url, headers=HEADERS)
        if tag_response.status_code != 200:
            print(f"Error: Unable to fetch annotated tag {tag} (status code: {tag_response.status_code})")
            return None
        annotated_tag = tag_response.json()
        return annotated_tag['object']['sha']

def export_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Tag', 'Commit Hash'])  # Write the header
        writer.writerows(data)  # Write the data

def main(owner, repo):
    tags = get_all_tags(owner, repo)
    if not tags:
        return

    tag_commit_pairs = []

    for tag in tags:
        tag_name = tag['name']
        commit_sha = get_commit_of_tag(owner, repo, tag_name)

        if commit_sha:
            tag_commit_pairs.append((tag_name, commit_sha))
        else:
            print(f"Could not find commit information for tag {tag_name}")

    # Export the results to a CSV file
    if tag_commit_pairs:
        export_to_csv(tag_commit_pairs, f'processed_data/attempt_2/{repo}_tags_commits.csv')
        print(f"Data exported to processed_data/attempt_2/{repo}_tags_commits.csv successfully.")

if __name__ == "__main__":
    # Replace with the owner and repository name
    OWNER = 'apache'  # e.g., 'octocat' for GitHub's sample repository
    REPO = 'hive'  # e.g., 'Hello-World'
    
    main(OWNER, REPO)
