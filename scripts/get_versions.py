import csv

# Initialize an empty list to store the valid tags
filtered_tags = []

# Open the CSV file
with open('processed_data/attempt_2/hive_tags_commits.csv', 'r') as file:  # Replace 'tags.csv' with your actual CSV file name
    reader = csv.reader(file)
    next(reader)  # Skip header row

    # Process each row
    for row in reader:
        tag = row[0]

        # Check if the tag contains a version of 2.0.0 or higher
        if "-2." in tag or "-3." in tag or "-4." in tag:  # Add more as needed for higher versions
            filtered_tags.append(tag)

# Output the filtered list of tags
print(len(filtered_tags))
