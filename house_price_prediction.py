# Step 1 : Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Step 2 : Load Dataset
df = pd.read_csv(r"C:\Users\Ashish\Downloads\house price preduction\data.csv")

# Step 3 : Show Dataset
print("Dataset Head:")
print(df.head())

# Step 4 : Data Cleaning
df = df.drop(["date","street","city","statezip","country"], axis=1, errors='ignore')

# Step 5 : Check Missing Values
df = df.dropna()

# Step 6 : Features and Target
X = df.drop("price", axis=1)
y = df["price"]

# Step 7 : Train Test Split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

# Step 8 : Model Training
model = LinearRegression()
model.fit(X_train,y_train)

# Step 9 : Prediction
pred = model.predict(X_test)

# Step 10 : Accuracy
print("Model Accuracy :", r2_score(y_test,pred))

# Step 11 : Graph
plt.scatter(y_test,pred)
plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("House Price Prediction")
plt.show()
