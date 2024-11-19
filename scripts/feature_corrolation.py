import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Load the dataset
def load_data(csv_file):
    # Load the CSV dataset
    df = pd.read_csv(csv_file)
    
    # Drop the 'Unnamed: 34' column as it is empty
    df = df.drop(columns=['Unnamed: 34'], errors='ignore')
    
    # Separate the features (X) and the target (y)
    X = df.drop(columns=['is_bug'])
    y = df['is_bug']
    
    return X, y

# Load the trained model
def load_model(pkl_file):
    # Load the Logistic Regression model from the pickle file
    with open(pkl_file, 'rb') as f:
        model = pickle.load(f)
    return model

# Train the Logistic Regression model if necessary (for testing purpose)
def train_model(X, y):
    # Standardize the features (important for logistic regression)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train a Logistic Regression model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_scaled, y)
    
    return model, scaler

# Analyze feature importance based on model coefficients
def analyze_feature_importance(model, X):
    # Logistic regression coefficients represent the feature importance
    coef = model.coef_[0]
    
    # Create a DataFrame with feature names and their corresponding coefficients
    feature_importance = pd.DataFrame({
        'Feature': X.columns,
        'Coefficient': coef
    })
    
    # Sort by the absolute value of coefficients to find the most important features
    feature_importance['Abs_Coefficient'] = np.abs(feature_importance['Coefficient'])
    feature_importance = feature_importance.sort_values(by='Abs_Coefficient', ascending=False)
    
    return feature_importance

# Visualize the feature importance and save the plot
def plot_feature_importance(feature_importance, output_file):
    # Plot the feature importance based on the coefficients
    plt.figure(figsize=(12, 8))  # Adjust figure size to prevent cropping
    
    # Create a horizontal bar plot
    plt.barh(feature_importance['Feature'], feature_importance['Coefficient'], color='skyblue')
    plt.xlabel('Coefficient Value')
    plt.title('Feature Importance in Bug Prediction')

    # Make sure there's enough space for feature labels
    plt.tight_layout()

    # Save the plot to a file
    plt.savefig(output_file)
    plt.close()
    print(f"Plot saved as {output_file}")

# Main function to load data, model, and analyze feature importance
def main(csv_file, pkl_file=None, output_file='feature_importance_plot.png'):
    # Load data
    X, y = load_data(csv_file)
    
    # If model file is provided, load it; otherwise, train a new model
    if pkl_file:
        model = load_model(pkl_file)
        print(f"Loaded model from {pkl_file}")
    else:
        print("No model file provided. Training a new model...")
        model, scaler = train_model(X, y)
        # Optionally save the trained model
        # with open('logistic_regression_model.pkl', 'wb') as f:
        #     pickle.dump(model, f)
        #     print("Model saved as logistic_regression_model.pkl")

    # Analyze feature importance
    feature_importance = analyze_feature_importance(model, X)
    
    # Print the feature importance (sorted from most to least influential)
    print("\nFeature Importance based on Logistic Regression Coefficients (most to least):")
    print(feature_importance[['Feature', 'Coefficient']])

    # Plot the feature importance and save the plot
    plot_feature_importance(feature_importance, output_file)

# Example usage
if __name__ == "__main__":
    # Specify the path to your CSV and pickle files
    csv_file = 'processed_data/attempt_2/cleaned_data.csv'  # Replace with your CSV file path
    pkl_file = 'processed_data/attempt_2/models_all_versions/logistic_regression_model.pkl'    # Replace with your model file path (optional)
    
    # Specify the output file path for the plot
    output_file = 'processed_data/attempt_2/results/feature_importance_plot.png'  # Change the file path or name if needed
    
    # Run the main function
    main(csv_file, pkl_file, output_file)
