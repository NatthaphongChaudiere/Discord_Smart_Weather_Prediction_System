import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Load Dataset in
df = pd.read_excel("Historical_Weather_Data.xlsx")
df.head()

# Check Data
df.info
df.describe()
df['condition'].value_counts()

# Handle Categorical Columns
le_wind = LabelEncoder()
df['wind_dir'] = le_wind.fit_transform(df['wind_dir'])

le_condition = LabelEncoder()
df['condition'] = le_condition.fit_transform(df['condition'])

# Define Features (X) and Target (y)
X = df.drop('condition', axis = 1)
y = df['condition']

# Splitting Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state= 42, shuffle=True)

# Train a model
model = RandomForestClassifier(n_estimators = 100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the Model
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save Model
with open("weather_prediction_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("le_wind.pkl", "wb") as f:
    pickle.dump(le_wind, f)

with open("le_condition.pkl", "wb") as f:
    pickle.dump(le_condition, f)

sample = {
    'temp_c': [27.5],
    'humidity': [20],
    'cloud': [21],
    'pressure_mb': [1009],
    'dewpoint_c': [24.2],
    'wind_kph': [1.4],
    'wind_dir': [le_wind.transform(['ESE'])[0]],
    'is_day': [1],
    'uv': [0]
}

sample_df = pd.DataFrame(sample)
predicted = model.predict(sample_df)
print("Predicted condition:", le_condition.inverse_transform(predicted)[0])
