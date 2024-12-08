
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

# Load the first dataset (primary dataset for initial training)
file1_path = 'fullclean_final1.csv'
data1 = pd.read_csv(file1_path)

# Select features and target from the first dataset
X1 = data1[['gender', 'highest_education', 'score', 'weight', 'activity_type']]
y1 = data1['final_result']

# Split the first dataset into training and testing sets
X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.2, random_state=42)

# Train the Logistic Regression model on the first dataset
model = LogisticRegression()
model.fit(X1_train, y1_train)

# Save the initially trained model
joblib.dump(model, 'initial_model.pkl')
print("Initial model trained on fullclean_final1 and saved.")

# Now load the second dataset (secondary dataset for fine-tuning)
file2_path = 'vdataset.csv'
data2 = pd.read_csv(file2_path)

# Select features and target from the second dataset (using corrected feature names)
X2 = data2[['gender', 'num_of_prev_attempts', 'assessment_score', 'total_task_completed', 
            'practical_hrs', 'theory_hrs', 'tot_completed_ex', 'indstry_training']]
y2 = data2['fina_grade']

# Split the second dataset into training and testing sets
X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size=0.2, random_state=42)

# Fine-tune the existing model on the second dataset
model.fit(X2_train, y2_train)

# Save the fine-tuned model
joblib.dump(model, 'fine_tuned_model.pkl')
print("Model fine-tuned on vdataset and saved.")
