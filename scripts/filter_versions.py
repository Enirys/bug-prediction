import pandas as pd

# Load the CSV file
df = pd.read_csv('processed_data/attempt_2/hive_tags_commits.csv')

# Define the list of tags to keep
predefined_tags = ['storage-release-2.8.1-rc2', 'storage-release-2.8.1-rc1', 
'storage-release-2.8.1-rc0', 'storage-release-2.8.0-rc0', 'storage-release-2.7.3-rc2', 'storage-release-2.7.3-rc1', 
'storage-release-2.7.3-rc0', 'storage-release-2.7.2-rc1', 'storage-release-2.7.2-rc0', 'storage-release-2.7.0-rc1', 
'storage-release-2.7.0-rc0', 'release-3.1.3-rc3', 'release-3.1.3-rc2', 'release-3.1.3-rc1', 'release-3.1.3-rc0', 
'release-3.1.2-rc0', 'release-2.3.10-rc1', 'release-2.3.10-rc0', 'release-2.3.9-rc0', 'release-2.3.8-rc3', 
'release-2.3.8-rc2', 'release-2.3.8-rc1', 'release-2.3.8-rc0', 'release-2.3.5-rc0', 'release-2.0.1', 'release-2.0.0', 
'rel/storage-release-2.8.1', 'rel/storage-release-2.7.3', 'rel/storage-release-2.7.2', 'rel/storage-release-2.7.1', 
'rel/storage-release-2.7.0', 'rel/storage-release-2.6.1', 'rel/storage-release-2.6.0', 'rel/storage-release-2.5.0', 
'rel/storage-release-2.4.0', 'rel/storage-release-2.3.1', 'rel/storage-release-2.3.0', 'rel/storage-release-2.2.1', 
'rel/storage-release-2.2.0', 'rel/standalone-metastore-release-3.0.0', 'rel/release-4.0.1', 'rel/release-4.0.0', 
'rel/release-4.0.0-beta-1', 'rel/release-4.0.0-alpha-2', 'rel/release-4.0.0-alpha-1', 'rel/release-3.1.3', 'rel/release-3.1.2', 
'rel/release-3.1.1', 'rel/release-3.1.0', 'rel/release-3.0.0', 'rel/release-2.3.10', 'rel/release-2.3.9', 'rel/release-2.3.8', 
'rel/release-2.3.7', 'rel/release-2.3.6', 'rel/release-2.3.5', 'rel/release-2.3.4', 'rel/release-2.3.3', 'rel/release-2.3.2', 
'rel/release-2.3.1', 'rel/release-2.3.0', 'rel/release-2.2.0', 'rel/release-2.1.1', 'rel/release-2.1.0', 'branch-3.1.3-rc0', 
'branch-3.1.2-rc0']

# Filter the DataFrame to only keep rows where the 'Tag' column is in the predefined list
filtered_df = df[df['Tag'].isin(predefined_tags)]

# Display or save the filtered DataFrame
print(filtered_df)

# Optionally, save the filtered data to a new CSV file
filtered_df.to_csv('processed_data/attempt_2/filtered_hive_tags_commits.csv', index=False)
