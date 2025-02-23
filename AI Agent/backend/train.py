import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Ucitavanje podataka
data = pd.read_excel('./anemia.xlsx')

# Priprema podataka
X = data[['Gender','RedPixel', 'GreenPixel', 'BluePixel', 'Hb']]
y = data['Anaemic'].apply(lambda x: 1 if x == 'Yes' else 0)

# Podjela na train i test skupove
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treniranje modela
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluacija
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f'Accuracy: {accuracy:.2f}')

# Cuvanje modela
joblib.dump(model, 'backend/anemia_model.joblib')