import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Page configuration
st.set_page_config(page_title="House Price Dashboard", page_icon="🏠", layout="wide")

# Title and description
st.title("🏠 House Price Prediction & Analytics Dashboard")
st.markdown("""
Welcome to the interactive House Price Analytics Dashboard. 
Explore the dataset, view interactive visualizations, and predict house prices using our Machine Learning model.
""")

# Load Dataset Function
@st.cache_data
def load_data():
    # Load dataset
    df = pd.read_csv(r"C:\Users\Ashish\Downloads\house price preduction\data.csv")
    
    # Data Cleaning
    df_clean = df.drop(["date", "street", "city", "statezip", "country"], axis=1, errors='ignore')
    df_clean = df_clean.dropna()
    return df, df_clean

# Load data
raw_df, clean_df = load_data()

# ----------------------------------------------------
# Sidebar - Navigation & Filters
# ----------------------------------------------------
st.sidebar.header("Navigation")
page = st.sidebar.radio("Navigate to:", ["Data Overview", "Interactive Analytics", "Price Predictor"])

# ----------------------------------------------------
# Page 1: Data Overview
# ----------------------------------------------------
if page == "Data Overview":
    st.header("📊 Data Overview")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Properties", f"{len(raw_df):,}")
    with col2:
        st.metric("Average Price", f"${raw_df['price'].mean():,.2f}")
    with col3:
        st.metric("Max Price", f"${raw_df['price'].max():,.2f}")
    with col4:
        st.metric("Avg Sqft Living", f"{raw_df['sqft_living'].mean():,.0f} sqft")

    # Display Raw Data
    st.subheader("Raw Dataset Preview")
    st.dataframe(raw_df.head(100)) # Show first 100 rows for performance
    
    # Display Clean Data Info
    st.subheader("Cleaned Data Features")
    st.write("For modeling and analytics, we use the following numerical features:")
    st.write(clean_df.columns.tolist())

# ----------------------------------------------------
# Page 2: Interactive Analytics (Power BI style)
# ----------------------------------------------------
elif page == "Interactive Analytics":
    st.header("📈 Interactive Analytics")
    
    # Filters
    st.sidebar.subheader("Filters")
    min_price = int(clean_df['price'].min())
    max_price = int(clean_df['price'].max())
    
    # Slider for price range
    price_range = st.sidebar.slider("Select Price Range:", min_value=min_price, max_value=max_price, value=(min_price, int(max_price/2)))
    
    # Slider for bedrooms
    bedroom_options = sorted(clean_df['bedrooms'].unique())
    selected_bedrooms = st.sidebar.multiselect("Select Bedrooms:", options=bedroom_options, default=bedroom_options)

    # Apply filters
    filtered_df = clean_df[
        (clean_df['price'] >= price_range[0]) & 
        (clean_df['price'] <= price_range[1]) &
        (clean_df['bedrooms'].isin(selected_bedrooms))
    ]

    st.write(f"Showing **{len(filtered_df)}** properties based on your filters.")

    # Charts Layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Scatter Plot: Price vs Sqft Living
        fig_scatter = px.scatter(
            filtered_df, 
            x="sqft_living", 
            y="price", 
            color="bedrooms",
            size="bathrooms",
            hover_data=["floors", "yr_built"],
            title="Price vs. Sqft Living (Size & Color encoded)",
            template="plotly_white"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Box Plot: Price by Condition
        fig_box = px.box(
            filtered_df, 
            x="condition", 
            y="price", 
            color="condition",
            title="Price Distribution by Property Condition",
            template="plotly_white"
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with col2:
        # Histogram: Price Distribution
        fig_hist = px.histogram(
            filtered_df, 
            x="price", 
            nbins=50, 
            title="Distribution of Property Prices",
            template="plotly_white",
            color_discrete_sequence=["indianred"]
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
        # Bar Chart: Average Price by Bedrooms
        avg_price_bed = filtered_df.groupby('bedrooms')['price'].mean().reset_index()
        fig_bar = px.bar(
            avg_price_bed, 
            x="bedrooms", 
            y="price", 
            title="Average Price by Number of Bedrooms",
            template="plotly_white",
            color="price",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_bar, use_container_width=True)


# ----------------------------------------------------
# Page 3: Price Predictor (ML Model)
# ----------------------------------------------------
elif page == "Price Predictor":
    st.header("🤖 Machine Learning Price Predictor")
    st.write("Enter the property details below to predict its estimated price using a Multiple Linear Regression model.")
    
    # Train Model
    X = clean_df.drop("price", axis=1)
    y = clean_df["price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    accuracy = r2_score(y_test, pred)
    
    st.info(f"Model Training Complete. Current R² Score (Accuracy): **{accuracy:.4f}**")
    st.markdown("---")
    
    st.subheader("Property Features Input")
    
    # Input Layout
    col1, col2, col3 = st.columns(3)
    
    # Create input fields based on feature columns
    input_data = {}
    
    with col1:
        input_data['bedrooms'] = st.number_input("Bedrooms", min_value=0.0, value=3.0, step=1.0)
        input_data['bathrooms'] = st.number_input("Bathrooms", min_value=0.0, value=2.0, step=0.25)
        input_data['sqft_living'] = st.number_input("Sqft Living", min_value=100.0, value=1500.0, step=100.0)
        input_data['sqft_lot'] = st.number_input("Sqft Lot", min_value=100.0, value=5000.0, step=100.0)
        
    with col2:
        input_data['floors'] = st.number_input("Floors", min_value=1.0, value=1.0, step=0.5)
        input_data['waterfront'] = st.selectbox("Waterfront", options=[0, 1], format_func=lambda x: "Yes" if x==1 else "No")
        input_data['view'] = st.number_input("View Quality (0-4)", min_value=0, max_value=4, value=0, step=1)
        input_data['condition'] = st.number_input("Condition (1-5)", min_value=1, max_value=5, value=3, step=1)
        
    with col3:
        input_data['sqft_above'] = st.number_input("Sqft Above", min_value=100.0, value=1500.0, step=100.0)
        input_data['sqft_basement'] = st.number_input("Sqft Basement", min_value=0.0, value=0.0, step=100.0)
        input_data['yr_built'] = st.number_input("Year Built", min_value=1900, max_value=2025, value=1990, step=1)
        input_data['yr_renovated'] = st.number_input("Year Renovated (0 if never)", min_value=0, max_value=2025, value=0, step=1)

    # Prediction Button
    if st.button("Predict Price", type="primary"):
        # Convert input dictionary to DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        
        # Display Result
        st.markdown("---")
        st.success(f"### Predicted Estimated Price: **${prediction:,.2f}**")
        
        st.balloons()
