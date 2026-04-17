import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

import pickle

# =========================
# LOAD DATASET
# =========================
df = pd.read_csv("dataset.csv")

# =========================
# DROP USELESS COLUMNS
# =========================
df = df.drop(columns=["Lead_ID", "Name"])

# =========================
# ENCODE TARGET
# =========================
df["Lead_Potential"] = df["Lead_Potential"].map({
    "Potential": 1,
    "Not Potential": 0
})

# =========================
# ENCODE CATEGORICAL FEATURES
# =========================
le_dict = {}

for col in df.columns:
    if df[col].dtype == 'object':
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        le_dict[col] = le

# =========================
# SPLIT DATA
# =========================
X = df.drop("Lead_Potential", axis=1)
y = df["Lead_Potential"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# TRAIN MODEL
# =========================
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

# =========================
# EVALUATE
# =========================
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", round(accuracy * 100, 2), "%")

# =========================
# SAVE MODEL + ENCODERS
# =========================
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(le_dict, open("encoders.pkl", "wb"))

print("Model Saved Successfully ✅")
