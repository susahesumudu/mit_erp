
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import joblib

# Load the first dataset (primary dataset for transfer learning)
file1_path = 'fullclean_final1.csv'
data1 = pd.read_csv(file1_path)

# Strip any leading/trailing spaces from column names
data1.columns = data1.columns.str.strip()

# Select features to normalize in the first dataset
features_to_normalize1 = ['gender', 'highest_education', 'score', 'weight', 'activity_type']

# Initialize the Min-Max scaler for the first dataset
scaler1 = MinMaxScaler()

# Fit the scaler to the first dataset's features
scaler1.fit(data1[features_to_normalize1])

# Save the first dataset's scaler
joblib.dump(scaler1, 'scaler_fullclean.pkl')
print("Scaler for fullclean_final dataset trained and saved.")

# Now load the second dataset (secondary dataset for fine-tuning)
file2_path = 'vdataset.csv'
data2 = pd.read_csv(file2_path)

# Strip any leading/trailing spaces from column names
data2.columns = data2.columns.str.strip()

# Encode categorical 'gender' column in the second dataset
label_encoder = LabelEncoder()
data2['gender'] = label_encoder.fit_transform(data2['gender'])

# Select features to normalize for the second dataset
features_to_normalize2 = ['gender', 'num_of_prev_attempts', 'assessment_score', 'total_task_completed', 
                          'practical_hrs', 'theory_hrs', 'tot_completed_ex', 'indstry_training']

# Initialize a separate Min-Max scaler for the second dataset
scaler2 = MinMaxScaler()

# Fit the scaler to the second dataset's features
scaler2.fit(data2[features_to_normalize2])

# Normalize the second dataset
normalized_data2 = scaler2.transform(data2[features_to_normalize2])

# Save the second dataset's scaler and normalized values
joblib.dump(scaler2, 'scaler_vdataset.pkl')
data2[features_to_normalize2] = normalized_data2
data2.to_csv('vdataset_normalized.csv', index=False)
print("vdataset normalized and saved.")
