import streamlit as st, pandas as pd
from sklearn.linear_model import LinearRegression

st.title("🏙️ Estate Analytics")

# 1. Load Data
df = pd.read_csv("data.csv").dropna()
X = df.drop(["price", "date", "street", "city", "statezip", "country"], axis=1, errors='ignore')

# 2. Train Model
m = LinearRegression().fit(X, df["price"])

# 3. Show Metrics & Chart
c1, c2 = st.columns(2)
c1.metric("Total Properties", len(df))
c2.metric("Avg Price", f"${df['price'].mean():,.0f}")
st.scatter_chart(df.head(100), x="sqft_living", y="price")

# 4. Predictor (Iterates dynamically over features)
st.subheader("🤖 Predict Price")
cols = st.columns(4)
i_d = {c: cols[i%4].number_input(c, value=float(X[c].median())) for i, c in enumerate(X.columns)}

if st.button("🌟 PREDICT", use_container_width=True, type="primary"):
    st.success(f"## 💰 Estimated Price: ${m.predict(pd.DataFrame([i_d]))[0]:,.2f}")
    st.balloons()
