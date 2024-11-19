import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score
import matplotlib.pyplot as plt
from sklearn2pmml import sklearn_to_pmml
from sklearn2pmml import make_pmml_pipeline
import pycox
from pycox.models import LogisticHazard
from pycox.preprocessing.feature_transforms import OneHot

# Step 1: Load the cleaned dataset
data = pd.read_csv('processed_data/attempt_2/cleaned_data.csv')

# Step 2: Check and remove the 'Unnamed: 34' column
if 'Unnamed: 34' in data.columns:
    data = data.drop(columns=['Unnamed: 34'])

# Step 3: Check for missing values
print("Number of missing values in each column:")
print(data.isnull().sum())

# Optionally, fill missing values with the mean of each column (if necessary)
data = data.fillna(data.mean())

# Step 4: Separate features (X) and target (y)
X = data.drop(columns=['is_bug'])  # Drop the 'is_bug' column from features
y = data['is_bug']  # 'is_bug' is the column indicating whether a bug is present (binary target)

# Step 5: Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 6: Standardize the features (important for Logistic Regression)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Step 7: Train the Logistic Regression model
log_reg = LogisticRegression(random_state=42, solver='liblinear')  # Specify solver for binary classification
log_reg.fit(X_train, y_train)

# Step 8: Make predictions on the test set
y_pred = log_reg.predict(X_test)

# Get predicted probabilities for the positive class (1)
y_pred_prob = log_reg.predict_proba(X_test)[:, 1]

# Step 9: Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

# Calculate the AUC
auc = roc_auc_score(y_test, y_pred_prob)

# Print model performance metrics
print("Model Performance Metrics:")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("Confusion Matrix:\n", conf_matrix)
print("AUC (Area Under the Curve):", auc)

# Step 10: Create the nomogram
# Convert the LogisticRegression model to a PMML format, which can then be used to create the nomogram
from sklearn2pmml import sklearn_to_pmml
from sklearn2pmml import make_pmml_pipeline

# Create the pipeline
pipeline = make_pmml_pipeline(
    ('scaler', StandardScaler()),
    ('model', log_reg)
)

# Save it as a PMML file
sklearn_to_pmml(pipeline, 'logistic_regression_model.pmml')

# You can now use external tools to create a nomogram from the PMML file, or you can generate a simple feature importance plot

# Step 11: Visualize the feature importance (simple version of nomogram)
import matplotlib.pyplot as plt
import numpy as np

# Get the feature names
feature_names = X.columns

# Get the coefficients from the logistic regression model
coefficients = log_reg.coef_[0]

# Sort the coefficients to plot them
sorted_idx = np.argsort(np.abs(coefficients))

# Create a bar chart to visualize feature importance
plt.figure(figsize=(10, 6))
plt.barh(range(len(sorted_idx)), coefficients[sorted_idx], align='center')
plt.yticks(range(len(sorted_idx)), [feature_names[i] for i in sorted_idx])
plt.xlabel('Coefficient Value')
plt.title('Feature Importance (Logistic Regression Coefficients)')
plt.show()
