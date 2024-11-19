import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import PartialDependenceDisplay

# Step 1: Load the dataset
data = pd.read_csv("processed_data/attempt_2/cleaned_data.csv")

# Drop the empty column 'Unnamed: 34'
data = data.drop(columns=["Unnamed: 34"])

# Display the first few rows to check the data
print(data.head())

# Step 2: Load the trained logistic regression model from the pickle file
model = joblib.load("processed_data/attempt_2/models_all_versions/logistic_regression_model.pkl")

# Step 3: Prepare the data for prediction (separate features and target)
X = data.drop(columns=["is_bug"])  # Features
y = data["is_bug"]  # Target (whether there is a bug or not)

# Step 4: Standardize the features (if the model was trained on standardized data)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 5: Create the Partial Dependence Plot (Nomogram)

# Use PartialDependenceDisplay to plot the results
fig, ax = plt.subplots(figsize=(12, 8))
disp = PartialDependenceDisplay.from_estimator(model, X_scaled, features=range(X.shape[1]), ax=ax)

# Add a title to the plot
ax.set_title("Partial Dependence Plot - Nomogram")

# Step 6: Save the Nomogram as an image
plt.savefig("processed_data/attempt_2/results/nomogram.png")

# Display the plot
plt.show()

# Print confirmation
print("Nomogram saved as 'nomogram.png'")
