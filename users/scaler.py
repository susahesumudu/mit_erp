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

# Convert categorical 'Gneder' to 'Gender'
label_encoder = LabelEncoder()
data2['Gender'] = label_encoder.fit_transform(data2['Gneder'])

# Select features to normalize for the second dataset
features_to_normalize2 = ['Gender', 'num_of_prev_attempts', 'assessment_score', 'Total Task Completed', 
                          'Practcials hrs', 'Theory hrs', 'Completed No Exersise', 'Idustry Training Experience']

# Fit the same scaler to the second dataset
scaler2 = MinMaxScaler()

# Fit the scaler to the second dataset's features
scaler2.fit(data2[features_to_normalize2])

# Save the second dataset's scaler for fine-tuning
joblib.dump(scaler2, 'scaler_vdataset.pkl')
print("Scaler for vdataset trained and saved.")

