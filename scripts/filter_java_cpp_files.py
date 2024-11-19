import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('processed_data/attempt_2/bug_file_associations.csv')

# Filter the DataFrame to include only .java and .cpp files (case insensitive)
filtered_df = df[df['File'].str.lower().str.endswith(('.java', '.cpp'))]

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv('processed_data/attempt_2/filtered_java_cpp_files.csv', index=False)

print("Filtered files have been saved to 'filtered_java_cpp_files.csv'")
