# model.py

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

data = {
    "glucose":[80,95,120,140,180],
    "haemoglobin":[14,13,12,11,10],
    "cholesterol":[150,180,220,240,280],
    "risk":[
        "Healthy",
        "Healthy",
        "Moderate Risk",
        "High Risk",
        "Critical Risk"
    ]
}

df = pd.DataFrame(data)

X = df[["glucose","haemoglobin","cholesterol"]]
y = df["risk"]

model = DecisionTreeClassifier()

model.fit(X,y)

pickle.dump(model, open("model.pkl","wb"))

print("Model Created")