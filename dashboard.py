import streamlit as st, pandas as pd
from sklearn.linear_model import LinearRegression

st.title("🏙️ Pune Real Estate Analytics")

# 1. Load Data
df = pd.read_csv("data.csv").dropna()

# Drop unnecessary columns but KEEP 'city'
base_df = df.drop(["price", "date", "street", "statezip", "country"], axis=1, errors='ignore')
X = pd.get_dummies(base_df, columns=["city"], drop_first=True)

# 2. Train Model
m = LinearRegression().fit(X, df["price"])

# 3. Show Metrics & Chart
c1, c2 = st.columns(2)
c1.metric("Total Properties", len(df))
c2.metric("Avg Price", f"${df['price'].mean():,.0f}")
st.scatter_chart(df.head(100), x="sqft_living", y="price")

# 4. Predictor (Pune-based)
st.subheader("🤖 Predict Price in Pune")

# Separate city input from numeric inputs
pune_areas = ["Baner", "Hinjewadi", "Kothrud", "Viman Nagar", "Wakad", "Kharadi", "Magarpatta", "Hadapsar", "Shivajinagar", "Pimpri"]
selected_city = st.selectbox("Select Area in Pune", sorted(pune_areas))

# Get numeric columns (everything except city)
numeric_cols = base_df.drop("city", axis=1).columns

cols = st.columns(4)
i_d = {}
for i, c in enumerate(numeric_cols):
    val_str = cols[i%4].text_input(c.title().replace("_", " "), value=str(int(base_df[c].median())))
    try:
        i_d[c] = float(val_str)
    except ValueError:
        i_d[c] = 0.0

i_d["city"] = selected_city

if st.button("🌟 PREDICT", use_container_width=True, type="primary"):
    # Convert user input to dataframe
    input_df = pd.DataFrame([i_d])
    
    # Apply dummy encoding for the selected city
    input_encoded = pd.get_dummies(input_df, columns=["city"])
    
    # Align the columns with the training data (fill missing city dummies with 0)
    input_encoded = input_encoded.reindex(columns=X.columns, fill_value=0)
    
    price_usd = m.predict(input_encoded)[0]
    price_inr = price_usd * 83.50  # Approximate conversion: 1 USD = 83.50 INR
    
    st.success(f"## 💰 Estimated Price for {selected_city}:\n### 💵 USD: **${price_usd:,.2f}**\n### 🇮🇳 INR: **₹{price_inr:,.2f}**")
    st.balloons()
