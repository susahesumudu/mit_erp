import pandas as pd
from sklearn.model_selection import train_test_split
import joblib

# Load the pre-trained model from the primary dataset
model = joblib.load('primary_model.pkl')

# Load the secondary dataset (vdataset.csv)
secondary_data = pd.read_csv('vdataset.csv')

# Strip any leading/trailing spaces from column names (just in case)
secondary_data.columns = secondary_data.columns.str.strip()

# Select features from the secondary dataset (matching the actual column names)
X_secondary = secondary_data[['gender', 'num_of_prev_attempts', 'assessment_score', 
                              'total_task_completed', 'practical_hrs', 'theory_hrs', 
                              'tot_completed_ex', 'indstry_training']]
y_secondary = secondary_data['fina_grade']

# Split the secondary dataset into training and testing sets
X_train_secondary, X_test_secondary, y_train_secondary, y_test_secondary = train_test_split(X_secondary, y_secondary, test_size=0.2, random_state=42)

# Fine-tune the existing model on the secondary dataset
model.fit(X_train_secondary, y_train_secondary)

# Save the fine-tuned model
joblib.dump(model, 'fine_tuned_model.pkl')

print("Model fine-tuned on secondary dataset and saved as fine_tuned_model.pkl.")

