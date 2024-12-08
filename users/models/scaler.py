import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import joblib

# Load the secondary dataset (vdataset.csv)
secondary_data = pd.read_csv('vdataset.csv')

# Strip any leading/trailing spaces from column names (just in case)
secondary_data.columns = secondary_data.columns.str.strip()

# Select features for scaling and model input
features = ['gender', 'num_of_prev_attempts', 'final_assessment_score', 'tasks_completed', 
            'practical_hours', 'theory_hours', 'exercises_completed', 'industry_training_experience']
X_secondary = secondary_data[features]
y_secondary = secondary_data['fina_grade']

# Scale the features using MinMaxScaler
scaler = MinMaxScaler()
X_secondary_scaled = scaler.fit_transform(X_secondary)

# Save the scaler for later use in prediction
joblib.dump(scaler, 'scaler_vdataset.pkl')

# Split the secondary dataset into training and testing sets
X_train_secondary, X_test_secondary, y_train_secondary, y_test_secondary = train_test_split(X_secondary_scaled, y_secondary, test_size=0.2, random_state=42)

# Load the primary model (trained on the primary dataset)
model_primary = joblib.load('primary_model.pkl')

# Fine-tune the model using the secondary dataset
model_primary.fit(X_train_secondary, y_train_secondary)

# Save the fine-tuned model
joblib.dump(model_primary, 'fine_tuned_model.pkl')
print("Model fine-tuned on secondary dataset and saved as 'fine_tuned_model.pkl'.")

