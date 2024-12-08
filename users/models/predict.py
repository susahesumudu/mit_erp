import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

# Load the primary dataset
primary_data = pd.read_csv('fullclean_final1.csv')

# Select features and target from the primary dataset
X_primary = primary_data[['gender', 'highest_education', 'score', 'weight', 'activity_type']]
y_primary = primary_data['final_result']

# Split the primary dataset into training and testing sets
X_train_primary, X_test_primary, y_train_primary, y_test_primary = train_test_split(X_primary, y_primary, test_size=0.2, random_state=42)

# Train the Logistic Regression model
model_primary = LogisticRegression()
model_primary.fit(X_train_primary, y_train_primary)

# Save the trained model
joblib.dump(model_primary, 'primary_model.pkl')
print("Primary model trained and saved as 'primary_model.pkl'.")

