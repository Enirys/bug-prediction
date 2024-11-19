import pandas as pd
import matplotlib.pyplot as plt

# Load your CSV file into a DataFrame
file_path = "processed_data/attempt_2/filtered_java_cpp_files.csv"  # Replace with the path to your actual CSV file
df = pd.read_csv(file_path)

# Step 1: Extract the file extensions and filter for only cpp and java files
df['File Extension'] = df['File'].str.extract(r'\.([a-zA-Z0-9]+)$')

# Filter for only cpp and java files
df_filtered = df[df['File Extension'].isin(['cpp', 'java'])]

# Step 2: Explode the "Affected Versions" column and clean up extra spaces
df_filtered_exploded = df_filtered.explode('Affected Version')
df_filtered_exploded['Affected Version'] = df_filtered_exploded['Affected Version'].str.strip()

# Step 3: Calculate the number of bugs per version and file extension combination
bugs_per_version_and_extension = df_filtered_exploded.groupby(['Affected Version', 'File Extension']).size().unstack(fill_value=0)

# Step 4: Plot the stacked bar chart
ax = bugs_per_version_and_extension.plot(kind='bar', stacked=True, figsize=(10, 7), color=['#FF6347', '#4682B4'], width=0.8)

# Add labels and title
plt.xlabel('Affected Version')
plt.ylabel('Number of Bugs')
plt.title('Number of Bugs per Affected Version and File Extension (Only cpp and java)')
plt.xticks(rotation=45)
plt.legend(title='File Extension', labels=['cpp', 'java'])
plt.tight_layout()

# Save the plot as a PNG file
plt.savefig('processed_data/attempt_2/data exploration/filtered_bugs_per_version_stacked_bar_chart.png')

# Show the plot
plt.show()
