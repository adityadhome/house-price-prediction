# Step 1: Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

print("--- House Price Prediction ML Pipeline ---")

# Step 2: Load Dataset
print("\n[1] Loading Dataset...")
df = pd.read_csv("data.csv")
print(f"Dataset Shape: {df.shape}")

# Step 3: Exploratory Data Analysis (EDA)
print("\n[2] Performing Exploratory Data Analysis...")
print("Data Types:\n", df.dtypes.head())
print("Summary Statistics:\n", df.describe().T[['mean', 'min', 'max']])

# Step 4: Data Cleaning
print("\n[3] Cleaning Data...")
# Drop non-numeric/text columns that are not useful for simple regression
df = df.drop(["date", "street", "statezip", "country"], axis=1, errors='ignore')

initial_rows = len(df)
df = df.dropna()
print(f"Dropped {initial_rows - len(df)} rows containing missing values.")

# Step 5: Assign Features (X) and Target (y)
print("\n[4] Defining Features and Target...")
X = df.drop("price", axis=1)
y = df["price"]

# Step 6: Train-Test Split
print("\n[5] Splitting Data into Training and Testing Sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training samples: {X_train.shape[0]} | Testing samples: {X_test.shape[0]}")

# Step 7: Feature Scaling (Standardization)
print("\n[6] Scaling Features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Step 8: Model Training
print("\n[7] Training Linear Regression Model...")
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Step 9: Predictions
print("\n[8] Making Predictions...")
pred = model.predict(X_test_scaled)

# Step 10: Model Evaluation
print("\n[9] Evaluating Model Performance...")
mae = mean_absolute_error(y_test, pred)
rmse = np.sqrt(mean_squared_error(y_test, pred))
r2 = r2_score(y_test, pred)

print(f"Mean Absolute Error (MAE): ${mae:,.2f}")
print(f"Root Mean Squared Error (RMSE): ${rmse:,.2f}")
print(f"R-squared (Accuracy): {r2 * 100:.2f}%")

# Step 11: Save the Model and Scaler
print("\n[10] Saving Model for Future Use...")
joblib.dump(model, "linear_regression_model.pkl")
joblib.dump(scaler, "scaler.pkl")
print("Model saved to 'linear_regression_model.pkl'")

# Step 12: Visualization
print("\n[11] Generating Visualizations...")
plt.figure(figsize=(10, 6))

# Plot identical relation line
plt.scatter(y_test, pred, alpha=0.5, color='blue', label="Predicted vs Actual")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label="Perfect Score Line")

plt.xlabel("Actual Price ($)", fontsize=12)
plt.ylabel("Predicted Price ($)", fontsize=12)
plt.title("House Price Prediction: Actual vs Predicted", fontsize=14)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save the plot securely
plt.savefig("prediction_accuracy.png")
print("Scatter plot saved to 'prediction_accuracy.png'")

plt.show()
