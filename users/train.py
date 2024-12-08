import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib

# Load the cleaned dataset (without 'Student No')
file_path = 'dataset.csv'
data = pd.read_csv(file_path)

# Select features and target (assuming 'FinalGrade' is the target variable)
X = data.drop(columns=['FinalGrade'])  # Adjust to match your target column name
y = data['FinalGrade']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# List of models to train
models = {
    "Logistic Regression": LogisticRegression(),
    "Random Forest": RandomForestClassifier(),
    "Gradient Boosting": GradientBoostingClassifier(),
    "Decision Tree": DecisionTreeClassifier(),
    "K-Nearest Neighbors": KNeighborsClassifier(),
    "Support Vector Machine": SVC(),
}

# Train each model and evaluate performance
best_model = None
best_accuracy = 0
best_model_name = ""

for name, model in models.items():
    # Train the model
    model.fit(X_train, y_train)
    
    # Predict on the test set
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"{name} Accuracy: {accuracy:.4f}")
    
    # Keep track of the best model
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model
        best_model_name = name

# Save the best model
model_output_path = f'{best_model_name}_model.pkl'
joblib.dump(best_model, model_output_path)

print(f"Best model: {best_model_name} with accuracy: {best_accuracy:.4f}")
print(f"Model saved to {model_output_path}")

