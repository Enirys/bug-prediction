import pandas as pd
import matplotlib.pyplot as plt
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.metrics import roc_curve, auc

# Load the data
data = pd.read_csv('processed_data/attempt_2/cleaned_data.csv')

# Remove unnecessary columns if they exist
if 'Unnamed: 34' in data.columns:
    data = data.drop(columns=['Unnamed: 34'])

# Fill missing values if needed
data = data.fillna(data.mean())

# Separate features (X) and target (y)
X = data.drop(columns=['is_bug'])
y = data['is_bug']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features for logistic regression
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train Logistic Regression model
lr = LogisticRegression(random_state=42)
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
y_pred_prob_lr = lr.predict_proba(X_test)[:, 1]

# Train Random Forest model
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
y_pred_prob_rf = rf.predict_proba(X_test)[:, 1]

# Calculate performance metrics for both models
metrics = {
    'Accuracy': [accuracy_score(y_test, y_pred_lr), accuracy_score(y_test, y_pred_rf)],
    'Precision': [precision_score(y_test, y_pred_lr), precision_score(y_test, y_pred_rf)],
    'Recall': [recall_score(y_test, y_pred_lr), recall_score(y_test, y_pred_rf)],
    'F1 Score': [f1_score(y_test, y_pred_lr), f1_score(y_test, y_pred_rf)],
    'AUC': [roc_auc_score(y_test, y_pred_prob_lr), roc_auc_score(y_test, y_pred_prob_rf)]
}

# Print metrics for each model to the console
print("Performance Metrics for Logistic Regression:")
print(f"  Accuracy:  {metrics['Accuracy'][0]:.4f}")
print(f"  Precision: {metrics['Precision'][0]:.4f}")
print(f"  Recall:    {metrics['Recall'][0]:.4f}")
print(f"  F1 Score:  {metrics['F1 Score'][0]:.4f}")
print(f"  AUC:       {metrics['AUC'][0]:.4f}\n")

print("Performance Metrics for Random Forest:")
print(f"  Accuracy:  {metrics['Accuracy'][1]:.4f}")
print(f"  Precision: {metrics['Precision'][1]:.4f}")
print(f"  Recall:    {metrics['Recall'][1]:.4f}")
print(f"  F1 Score:  {metrics['F1 Score'][1]:.4f}")
print(f"  AUC:       {metrics['AUC'][1]:.4f}\n")

# Convert the metrics to a DataFrame for easier plotting
metrics_df = pd.DataFrame(metrics, index=['Logistic Regression', 'Random Forest'])

# Define distinct colors for each metric
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']  # Blue, Orange, Green, Red, Purple

# Plot the metrics comparison as a grouped bar chart
metrics_df.plot(kind='bar', figsize=(10, 6), color=colors, edgecolor='black')
plt.title('Comparaison des perforamnces: Logistic Regression vs Random Forest')
plt.ylabel('Score')
plt.xticks(rotation=0)
plt.legend(title="Metric", loc="upper left")
plt.ylim(0, 1)  # assuming the metrics range from 0 to 1

# Save the plot
#plt.savefig('processed_data/attempt_2/results/performance_comparison.png', format='png', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()

# Save the models
"""
with open('processed_data/attempt_2/models/logistic_regression_model.pkl', 'wb') as lr_file:
    pickle.dump(lr, lr_file)

with open('processed_data/attempt_2/models/random_forest_model.pkl', 'wb') as rf_file:
    pickle.dump(rf, rf_file)

print("Models saved as 'logistic_regression_model.pkl' and 'random_forest_model.pkl'")
"""

# Compute ROC curve and AUC for Logistic Regression
fpr_lr, tpr_lr, _ = roc_curve(y_test, y_pred_prob_lr)
roc_auc_lr = auc(fpr_lr, tpr_lr)

# Compute ROC curve and AUC for Random Forest
fpr_rf, tpr_rf, _ = roc_curve(y_test, y_pred_prob_rf)
roc_auc_rf = auc(fpr_rf, tpr_rf)

# Plot the ROC curves
plt.figure(figsize=(10, 6))
plt.plot(fpr_lr, tpr_lr, color='blue', lw=2, label=f'Logistic Regression (AUC = {roc_auc_lr:.2f})')
plt.plot(fpr_rf, tpr_rf, color='green', lw=2, label=f'Random Forest (AUC = {roc_auc_rf:.2f})')

# Plot the diagonal line for random guess
plt.plot([0, 1], [0, 1], color='gray', linestyle='--')

# Labels and title
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")

# Save the ROC curve plot
plt.savefig('processed_data/attempt_2/results/roc_curve_comparison.png', format='png', dpi=300, bbox_inches='tight')

# Display the ROC plot
plt.show()