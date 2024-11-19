import requests
import os

# List of numbers to create pagination URLs
pagination_numbers = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]

# Base URLs
base_url = "https://issues.apache.org/jira/sr/jira.issueviews:searchrequest-csv-all-fields/temp/SearchRequest.csv?jqlQuery=project+%3D+HIVE+AND+issuetype+%3D+Bug+AND+status+in+%28Resolved%2C+Closed%29+ORDER+BY+priority+DESC%2C+updated+DESC&delimiter=,&tempMax=1000"
pagination_url_template = "https://issues.apache.org/jira/sr/jira.issueviews:searchrequest-csv-all-fields/temp/SearchRequest.csv?jqlQuery=project+%3D+HIVE+AND+issuetype+%3D+Bug+AND+status+in+%28Resolved%2C+Closed%29+ORDER+BY+priority+DESC%2C+updated+DESC&delimiter=,&pager/start={num}&tempMax=1000"

# Directory to save downloaded files
download_directory = "raw_data/all_fields_data_raw_versions"
os.makedirs(download_directory, exist_ok=True)

# Function to download a file
def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {url} (Status Code: {response.status_code})")

# Download the first URL
download_file(base_url, os.path.join(download_directory, "SearchRequest_0.csv"))

# Download the paginated URLs
for num in pagination_numbers:
    paginated_url = pagination_url_template.format(num=num)
    download_file(paginated_url, os.path.join(download_directory, f"SearchRequest_{num}.csv"))
