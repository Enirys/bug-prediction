import pandas as pd

# Load the CSV file
df = pd.read_csv("processed_data/attempt_2/metrics_All_versions_exo_2b.csv", sep=";")

# Filter out rows that consist only of semicolons (empty values)
df_cleaned = df.dropna(how="all")

# Save the cleaned CSV to a new file
df_cleaned.to_csv("processed_data/attempt_2/cleaned_file.csv", index=False, sep=";")
