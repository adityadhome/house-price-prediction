# PROJECT DOCUMENTATION
## House Price Prediction and Analytics Dashboard Using Machine Learning

---

## 1. ABSTRACT
The Real Estate industry is one of the most unpredictable and highly volatile sectors. Predicting property prices manually is prone to human error and bias. The primary objective of this project is to analyze historical real estate data and develop a Machine Learning (ML) model capable of predicting house prices with high accuracy based on various housing features. Furthermore, this project implements an interactive Web Dashboard allowing end-users to predict prices by selecting specific areas (e.g., Pune areas) and features seamlessly.

## 2. INTRODUCTION
With globalization and rapid urbanization, investing in real estate has become highly lucrative. However, buyers and sellers often face a pricing dilemma. This project solves this using a predictive model. By leveraging Multiple Linear Regression, the system learns the impact of various housing attributes (like the number of bedrooms, bathrooms, total living area squared footage, and condition of the house). A clean, modern Front-End is provided via the Streamlit Python framework to demonstrate practical software engineering.

## 3. SYSTEM REQUIREMENTS
### 3.1 Hardware Requirements
* **Processor:** Minimum Intel Core i3 / AMD Ryzen 3 or above.
* **RAM:** 4 GB (8 GB recommended for faster ML model training).
* **Storage:** 1 GB free disk space.

### 3.2 Software Requirements
* **Operating System:** Windows 10/11, macOS, or Linux.
* **Programming Language:** Python 3.8+
* **Libraries/Packages:** 
  * `pandas`, `numpy` (Data Processing)
  * `scikit-learn` (Machine Learning algorithms)
  * `matplotlib`, `seaborn` (Data Visualization)
  * `streamlit` (Web App Framework)
* **IDE:** VS Code / Jupyter Notebook / PyCharm.

## 4. SYSTEM ARCHITECTURE & METHODOLOGY
The system is divided into two primary scripts:
1. **Backend ML Pipeline (`house_price_prediction.py`)**
2. **Frontend UI System (`dashboard.py`)**

### 4.1 Data Processing & Cleaning
The raw data (`data.csv`) is first imported using Pandas. Irrelevant columns (e.g., strings containing simple dates or street addresses) are removed to avoid confusing the regression model. Any rows with missing or 'NaN' values are dropped to maintain training integrity.

### 4.2 Feature Engineering (One-Hot Encoding)
Categorical features, such as "City/Area," cannot be mathematically interpreted by our Regression model. To solve this, **Dummy Encoding (pd.get_dummies)** is employed. It splits the categorical column into multiple binary columns (1s and 0s) to map location features mathematically.

### 4.3 Training the Model
The dataset is split into two parts:
* **Training Data (80%)**: Used by the algorithm to understand the patterns.
* **Testing Data (20%)**: Hidden from the model during training, used later to test if the model's predictions are accurate.
* **StandardScaler**: Used to scale/normalize all numeric values so large numbers (like sqft) don't unfairly overpower small numbers (like bedrooms).

### 4.4 The Algorithm (Linear Regression)
The project utilizes `sklearn.linear_model.LinearRegression`. It creates an N-dimensional hyperplane that minimizes the total residual errors (differences between actual target prices and predicted prices).

## 5. IMPLEMENTATION DETAILS
* **`dashboard.py`**: Streamlit is leveraged to abstract the complex Python console into an interactive Web Page. A `st.selectbox` allows the user to select localized Cities/Areas (such as Baner, Viman Nagar, etc.), while input boxes accept specific numeric dimensions for the house.
* **Prediction Logic**: When the user clicks "PREDICT", a custom DataFrame is generated, Dummy columns are matched via `reindex(fill_value=0)`, and the `m.predict()` function executes the estimation. The output is then cleanly converted to INR (₹) using an active conversion multiplier.

## 6. RESULTS & EVALUATION
The model produces impressive results during evaluation against the 20% test data.
* **MAE (Mean Absolute Error):** Calculated to observe the median margin of deviation.
* **RMSE (Root Mean Square Error):** Calculated to penalize unusually large errors.
* **Visualization:** The system generates a `prediction_accuracy.png` scatter plot. The X-axis represents the Actual Prices while the Y-axis represents the Model's Predicted Prices. A prominent red diagonal 'perfect fit line' is drawn, showcasing that the plotted blue tests successfully group around the identity correlation factor.

## 7. CONCLUSION
This project successfully converges core Machine Learning data-science with an easy, lightweight Web Engineering framework. The application runs robustly and can instantly formulate property estimations removing any requirement for manual human property valuation. It is a perfect step forward for modern Real Estate technological disruption.

## 8. BIBLIOGRAPHY/REFERENCES
1. Scikit-Learn Documentation (https://scikit-learn.org/)
2. Streamlit Documentation (https://docs.streamlit.io/)
3. Pandas Data manipulation (https://pandas.pydata.org/)
4. Python Official Documentation (https://docs.python.org/3/)
