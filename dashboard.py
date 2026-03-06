import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

st.set_page_config(page_title="Premium House Pricing", page_icon="�️", layout="wide")

# Custom aesthetic styling
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #FF6B6B, #556270);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        text-align: center;
        padding-top: 20px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #888888;
        margin-bottom: 40px;
        text-align: center;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem;
        color: #FF6B6B;
    }
    div[data-testid="stMetric"] {
        background-color: rgba(200, 200, 200, 0.1);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid rgba(200, 200, 200, 0.2);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🏙️ Premium Estate Analytics</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Property Insights & Price Predictions Dashboard</p>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\Ashish\Downloads\house price preduction\data.csv")
    df_clean = df.drop(["date", "street", "city", "statezip", "country"], axis=1, errors='ignore')
    df_clean = df_clean.dropna()
    return df, df_clean

raw_df, clean_df = load_data()

# Model Training
@st.cache_resource
def train_model(data):
    X = data.drop("price", axis=1)
    y = data["price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    accuracy = r2_score(y_test, pred)
    return model, accuracy, X.columns

model, accuracy, feature_cols = train_model(clean_df)

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Properties", f"{len(raw_df):,}")
col2.metric("Average Price", f"${raw_df['price'].mean():,.0f}")
col3.metric("Max Price", f"${raw_df['price'].max():,.0f}")
col4.metric("Avg Living Space", f"{raw_df['sqft_living'].mean():,.0f} sqft")

st.markdown("<br><hr>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📈 Deep Analytics", "🔎 Data Explorer", "🤖 AI Price Predictor"])

with tab1:
    col_filter, col_charts = st.columns([1, 4])
    with col_filter:
        st.subheader("Filter Data")
        min_price = int(clean_df['price'].min())
        max_price = int(clean_df['price'].max())
        
        price_range = st.slider("Price Range ($)", min_price, max_price, (min_price, int(max_price/3)))
        bedrooms = st.multiselect("Bedrooms", sorted(clean_df['bedrooms'].unique()), default=[2,3,4,5])
        
        filtered_df = clean_df[
            (clean_df['price'] >= price_range[0]) & 
            (clean_df['price'] <= price_range[1]) &
            (clean_df['bedrooms'].isin(bedrooms))
        ]
        st.info(f"Showing **{len(filtered_df):,}** properties")

    with col_charts:
        tab_a, tab_b = st.tabs(["Price Distribution", "Space Analysis"])
        with tab_a:
            fig1 = px.histogram(
                filtered_df, x="price", nbins=40,
                color_discrete_sequence=['#FF6B6B'],
                title="Property Price Distribution",
                template="plotly"
            )
            fig1.update_layout(bargap=0.1)
            st.plotly_chart(fig1, use_container_width=True)
            
            # Average Price by Condition
            avg_cond = filtered_df.groupby('condition')['price'].mean().reset_index()
            fig2 = px.bar(
                avg_cond, x='condition', y='price',
                color='price', color_continuous_scale='Sunsetdark',
                title="Average Price by Property Condition",
                template="plotly"
            )
            st.plotly_chart(fig2, use_container_width=True)

        with tab_b:
            fig3 = px.scatter(
                filtered_df, x="sqft_living", y="price", 
                color="bedrooms", size="bathrooms",
                color_continuous_scale="Teal",
                hover_data=["floors", "yr_built"],
                title="Price vs Living Area (Bubble size = Bathrooms)",
                template="plotly"
            )
            st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.subheader("Raw Data Explorer")
    st.dataframe(raw_df.head(500), use_container_width=True)

with tab3:
    st.subheader("🤖 AI Price Predictor")
    st.markdown("Adjust the controls below to estimate the exact value of a property based on its features using Machine Learning.")
    
    st.info(f"Model Accuracy (R² Score): **{accuracy*100:.1f}%**")
    
    st.markdown('<div style="padding: 20px; background-color: rgba(200, 200, 200, 0.05); border-radius: 10px; border: 1px solid rgba(200, 200, 200, 0.2);">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    input_data = {}
    
    with c1:
        input_data['bedrooms'] = st.slider("Bedrooms", 1, 10, 3)
        input_data['bathrooms'] = st.slider("Bathrooms", 1.0, 8.0, 2.0, 0.25)
        input_data['sqft_living'] = st.slider("Sqft Living", 500, 10000, 2000, 100)
        input_data['sqft_lot'] = st.number_input("Sqft Lot", 500, 100000, 5000, 500)
        
    with c2:
        input_data['floors'] = st.slider("Floors", 1.0, 3.5, 1.0, 0.5)
        input_data['waterfront'] = st.radio("Waterfront", [0, 1], format_func=lambda x: "Yes" if x==1 else "No")
        input_data['view'] = st.slider("View Quality", 0, 4, 0)
        input_data['condition'] = st.slider("Condition", 1, 5, 3)
        
    with c3:
        input_data['sqft_above'] = st.number_input("Sqft Above", 500, 10000, 1500, 100)
        input_data['sqft_basement'] = st.slider("Sqft Basement", 0, 3000, 0, 100)
        input_data['yr_built'] = st.slider("Year Built", 1900, 2025, 1990)
        input_data['yr_renovated'] = st.slider("Year Renovated (0 if never)", 0, 2025, 0)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🌟 GET PREDICTED ESTIMATE 🌟", use_container_width=True, type="primary"):
        with st.spinner("Analyzing real estate market data..."):
            input_df = pd.DataFrame([input_data])
            # Ensure column order matches feature_cols
            input_df = input_df[feature_cols]
            prediction = model.predict(input_df)[0]
            
            st.markdown(f"""
            <div style="background: -webkit-linear-gradient(135deg, #FF6B6B, #556270); padding: 40px; border-radius: 15px; text-align: center; box-shadow: 0px 10px 20px rgba(0,0,0,0.2); margin-top:20px;">
                <h3 style="color: rgba(255,255,255,0.9); margin: 0; font-family: sans-serif;">Estimated Property Market Value</h3>
                <h1 style="color: white; font-size: 5rem; margin: 15px 0; font-family: monospace; font-weight: 800;">${prediction:,.2f}</h1>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
