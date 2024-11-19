import os
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score

# Step 1: Define the folder containing the CSV files
folder_path = 'processed_data/attempt_2/split_by_version_clean'  # Folder containing the CSV files
output_model_folder = 'processed_data/attempt_2/models_per_version'  # Folder where models will be saved
output_plot_folder = 'processed_data/attempt_2/metrics_plots_versions'  # Folder where plots will be saved

# Create the output model folder and plot folder if they don't exist
os.makedirs(output_model_folder, exist_ok=True)
os.makedirs(output_plot_folder, exist_ok=True)

# Step 2: Loop through all CSV files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):  # Check if the file is a CSV file
        file_path = os.path.join(folder_path, filename)
        print(f"Processing file: {filename}")

        # Load the dataset
        data = pd.read_csv(file_path)

        # Step 3: Check and remove the 'Unnamed: 34' column if it exists
        if 'Unnamed: 34' in data.columns:
            data = data.drop(columns=['Unnamed: 34'])

        # Step 4: Check for missing values
        print(f"Number of missing values in {filename}:")
        print(data.isnull().sum())

        # Handle columns with all NaN values or missing values by dropping them
        data = data.dropna(axis=1, how='all')  # Drop columns with all NaN values

        # Fill missing values with the mean of each column
        data = data.fillna(data.mean())

        # Ensure no missing values remain
        if data.isnull().sum().sum() > 0:
            print(f"Warning: There are still missing values in the dataset for {filename}")
        else:
            print(f"No missing values remain in the dataset for {filename}")

        # Step 5: Separate features (X) and target (y)
        X = data.drop(columns=['is_bug'])  # Drop the 'is_bug' column from features
        y = data['is_bug']  # 'is_bug' is the target (binary)

        # Step 6: Split the data into training and testing sets (80% train, 20% test)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Step 7: Standardize the features
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        # Step 8: Train the Logistic Regression model
        log_reg = LogisticRegression(random_state=42, solver='liblinear')
        try:
            log_reg.fit(X_train, y_train)
        except ValueError as e:
            print(f"Error while fitting model for {filename}: {e}")
            continue  # Skip this file if an error occurs

        # Step 9: Make predictions on the test set
        y_pred = log_reg.predict(X_test)

        # Get predicted probabilities for the positive class (1)
        y_pred_prob = log_reg.predict_proba(X_test)[:, 1]

        # Step 10: Evaluate the model
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)

        # Calculate the AUC (Area Under the Curve)
        auc = roc_auc_score(y_test, y_pred_prob)

        # Print model performance metrics
        print(f"Model Performance for {filename}:")
        print("Accuracy:", accuracy)
        print("Precision:", precision)
        print("Recall:", recall)
        print("F1 Score:", f1)
        print("Confusion Matrix:\n", conf_matrix)
        print("AUC (Area Under the Curve):", auc)

        # Step 11: Save the trained model using pickle
        model_filename = os.path.join(output_model_folder, f"model_{os.path.splitext(filename)[0]}.pkl")
        with open(model_filename, 'wb') as model_file:
            pickle.dump(log_reg, model_file)
        print(f"Saved model for {filename} at {model_filename}\n")

        # Step 12: Create a bar plot of the model performance metrics
        metrics = ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'AUC']
        scores = [accuracy, precision, recall, f1, auc]

        # Create the bar plot
        plt.figure(figsize=(8, 6))
        plt.bar(metrics, scores, color=['blue', 'green', 'orange', 'red', 'purple'])
        plt.title(f'Model Performance Metrics - {filename}')
        plt.xlabel('Metrics')
        plt.ylabel('Scores')
        plt.ylim(0, 1)  # Set the y-axis limit from 0 to 1 for normalized metrics

        # Save the plot to a file
        plot_filename = os.path.join(output_plot_folder, f"metrics_{os.path.splitext(filename)[0]}.png")
        plt.tight_layout()  # Adjust layout to avoid clipping
        plt.savefig(plot_filename)
        plt.close()  # Close the plot to avoid memory issues

        print(f"Saved plot for {filename} at {plot_filename}\n")
