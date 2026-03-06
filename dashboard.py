import streamlit as st, pandas as pd, plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Premium Estate", page_icon="🏙️", layout="wide")
st.markdown("<style>.main-header{font-size:3rem;font-weight:900;background:-webkit-linear-gradient(45deg,#FF6B6B,#556270);-webkit-text-fill-color:transparent;text-align:center}</style><p class='main-header'>🏙️ Estate Analytics</p>", unsafe_allow_html=True)

@st.cache_data
def get_data():
    df = pd.read_csv(r"C:\Users\Ashish\Downloads\house price preduction\data.csv").dropna()
    return df, df.drop(["date", "street", "city", "statezip", "country"], axis=1, errors='ignore')

r_df, c_df = get_data()

@st.cache_resource
def get_model(df):
    X, y = df.drop("price", axis=1), df["price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    m = LinearRegression().fit(X_train, y_train)
    return m, m.score(X_test, y_test), X.columns

model, acc, cols = get_model(c_df)

c1, c2, c3 = st.columns(3)
c1.metric("Properties", f"{len(r_df):,}")
c2.metric("Avg Price", f"${r_df['price'].mean():,.0f}")
c3.metric("Max Price", f"${r_df['price'].max():,.0f}")

t1, t2, t3 = st.tabs(["📈 Analytics", "🔎 Data", "🤖 Predictor"])

with t1:
    c_f, c_c = st.columns([1, 4])
    rng = c_f.slider("Price", int(c_df['price'].min()), int(c_df['price'].max()), (0, 1000000))
    beds = c_f.multiselect("Beds", sorted(c_df['bedrooms'].unique()), [2,3,4,5])
    f_df = c_df[(c_df['price'] >= rng[0]) & (c_df['price'] <= rng[1]) & (c_df['bedrooms'].isin(beds))]
    c_f.info(f"{len(f_df):,} properties")
    
    ta, tb = c_c.tabs(["Distribution", "Space"])
    
    # Dynamic Color Histogram/Bar
    fig_hist = px.histogram(f_df, x="price", nbins=40, color="bedrooms",
                            title="Price Dist (Colored by Bedrooms)")
    ta.plotly_chart(fig_hist, use_container_width=True)
    
    # Dynamic Color Scatter Plot
    fig_scatter = px.scatter(f_df, x="sqft_living", y="price", color="price", size="bedrooms", 
                             color_continuous_scale="RdYlBu_r", title="Price vs Living Area (Red=High)")
    tb.plotly_chart(fig_scatter, use_container_width=True)

with t2:
    n = st.slider("Rows", 10, 100, 20, 5)
    st.dataframe(r_df.head(n), use_container_width=True)

with t3:
    st.info(f"Model Accuracy: {acc*100:.1f}%")
    i_d = {
        'bedrooms': st.slider("Beds", 1, 10, 3), 'bathrooms': st.slider("Baths", 1.0, 8.0, 2.0, 0.5),
        'sqft_living': st.slider("Sqft Living", 500, 10000, 2000, 100), 'sqft_lot': st.number_input("Sqft Lot", value=5000),
        'floors': st.slider("Floors", 1.0, 3.5, 1.0, 0.5), 'waterfront': st.radio("Waterfront", [0, 1]),
        'view': st.slider("View", 0, 4, 0), 'condition': st.slider("Condition", 1, 5, 3),
        'sqft_above': st.number_input("Sqft Above", value=1500), 'sqft_basement': st.slider("Sqft Basement", 0, 3000, 0),
        'yr_built': st.slider("Year Built", 1900, 2025, 1990), 'yr_renovated': st.slider("Renovated (0 if never)", 0, 2025, 0)
    }
    if st.button("🌟 PREDICT", use_container_width=True, type="primary"):
        pred = model.predict(pd.DataFrame([i_d])[cols])[0]
        st.markdown(f"<div style='background:#FF6B6B;padding:20px;border-radius:10px;text-align:center'><h1 style='color:white'>${pred:,.2f}</h1></div>", unsafe_allow_html=True)
        st.balloons()
