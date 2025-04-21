import streamlit as st
import pandas as pd
import numpy as np
import pickle
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Crop Yield Predictor",
    page_icon="🌾",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2e7d32;
        text-align: center;
    }
    .subheader {
        font-size: 1.2rem;
        color: #558b2f;
        text-align: center;
    }
    .info-text {
        background-color: #f1f8e9;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .prediction-box {
        background-color: #e8f5e9;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-top: 1rem;
    }
    .stButton>button {
        background-color: #4caf50;
        color: white;
        font-weight: bold;
        padding: 0.5rem 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Load the model
@st.cache_resource
def load_model():
    return pickle.load(open('model.pkl', 'rb'))

try:
    model = load_model()
    model_loaded = True
except Exception as e:
    st.error(f"Failed to load model: {str(e)}")
    model_loaded = False

# App header
st.markdown("<h1 class='main-header'>🌾 Crop Yield Prediction</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Optimize your farming with data-driven predictions</p>", unsafe_allow_html=True)

# Create two columns for the layout
col1, col2 = st.columns([2, 1])

with col1:
  
    st.markdown("""
    ### How it works
    This tool uses machine learning to predict crop yields based on environmental and agricultural factors.
    Fill in the form with your specific conditions to get an estimated yield in tons per hectare.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Input form
    with st.form("prediction_form"):
        st.subheader("📊 Farm Data")
        
        # Create layout for form fields
        form_col1, form_col2 = st.columns(2)
        
        with form_col1:
            region = st.selectbox("Region", ['West', 'South', 'North', 'East'], 
                                index=0, help="Select the geographical region of your farm")
            soil_type = st.selectbox("Soil Type", 
                                    ['Sandy', 'Clay', 'Loam', 'Silt', 'Clay Loam', 'Sandy Loam', 'Other'],
                                    help="Select the primary soil type of your field")
            crop = st.selectbox("Crop Type", 
                                ['Wheat', 'Rice', 'Maize', 'Potato', 'Soybean', 'Cotton', 'Sugarcane', 'Other'],
                                help="Select the crop you're planning to grow")
        
        with form_col2:
            weather_condition = st.selectbox("Predominant Weather", 
                                            ['Sunny', 'Rainy', 'Cloudy', 'Mixed'],
                                            help="Select the typical weather condition during growing season")
            fertilizer_used = st.radio("Fertilizer Used", ['Yes', 'No'], horizontal=True,
                                    help="Will you use fertilizer?")
            irrigation_used = st.radio("Irrigation Used", ['Yes', 'No'], horizontal=True,
                                    help="Will you use irrigation?")
        
        st.subheader("📈 Environmental Factors")
        env_col1, env_col2 = st.columns(2)
        
        with env_col1:
            # Changed from slider to text input
            rainfall = st.text_input("Average Rainfall (mm)", 
                                    value="500",
                                    help="Expected average rainfall during the growing season")
            
            # Changed from slider to text input
            temperature = st.text_input("Average Temperature (°C)", 
                                      value="25",
                                      help="Expected average temperature during the growing season")
        
        with env_col2:
            # Changed from slider to text input
            days_to_harvest = st.text_input("Days to Harvest", 
                                         value="120",
                                         help="Expected number of days from planting to harvest")
        
        submitted = st.form_submit_button("🔍 Predict Yield")

with col2:
    if model_loaded:
        
        st.subheader("📝 Recent Predictions")
        
        # Display some dummy recent predictions
        recent_data = {
            "Crop": ["Wheat", "Rice", "Maize"],
            "Region": ["North", "South", "West"],
            "Yield": [4.2, 5.7, 6.3]
        }
        
        df = pd.DataFrame(recent_data)
        df['Yield'] = df['Yield'].apply(lambda x: f"{x} tons/ha")
        st.dataframe(df, hide_index=True, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Add some tips or educational content
        st.subheader("💡 Farming Tips")
        with st.expander("Optimal Growing Conditions"):
            st.write("""
            - Wheat: 15-20°C, moderate rainfall
            - Rice: 20-25°C, high rainfall
            - Maize: 18-25°C, moderate rainfall
            - Potato: 15-20°C, moderate rainfall
            """)
        
        with st.expander("Soil Health Tips"):
            st.write("""
            - Rotate crops yearly to prevent nutrient depletion
            - Consider cover crops during off-seasons
            - Test soil pH and nutrient levels regularly
            - Add organic matter to improve soil structure
            """)

# Handle prediction when form is submitted
if submitted and model_loaded:
    # Validation and conversion - same as your original logic
    def to_float(val, name):
        try:
            return float(val)
        except:
            st.warning(f"⚠️ Invalid input for {name}. Using NaN.")
            return np.nan
    
    # Using the same validation approach from your original code
    features = {
        'Region': region,
        'Soil_Type': soil_type,
        'Crop': crop,
        'Rainfall_mm': to_float(rainfall, 'Rainfall'),
        'Temperature_Celsius': to_float(temperature, 'Temperature'),
        'Fertilizer_Used': fertilizer_used == 'Yes',
        'Irrigation_Used': irrigation_used == 'Yes',
        'Weather_Condition': weather_condition,
        'Days_to_Harvest': to_float(days_to_harvest, 'Days to Harvest')
    }

    input_df = pd.DataFrame([features])
    
    # For demonstration, display the inputs
    st.subheader("📋 Your Input Summary")
    display_df = pd.DataFrame([{
        "Region": region,
        "Crop": crop,
        "Soil Type": soil_type,
        "Rainfall": f"{to_float(rainfall, 'Rainfall')} mm",
        "Temperature": f"{to_float(temperature, 'Temperature')} °C",
        "Days to Harvest": int(to_float(days_to_harvest, 'Days to Harvest')) if not np.isnan(to_float(days_to_harvest, 'Days to Harvest')) else np.nan
    }])
    st.dataframe(display_df, hide_index=True, use_container_width=True)

    # Show a spinner during prediction
    with st.spinner('Calculating yield prediction...'):
        try:
            # Make prediction
            prediction = model.predict(input_df)
            yield_value = prediction[0]
            
            # Display result
            
            st.markdown(f"### Predicted Yield: **{yield_value:.2f} tons/hectare**")
            
            # Add some interpretation
            if yield_value > 8:
                st.markdown("✨ **Excellent yield potential!** Your conditions are optimal for this crop.")
            elif yield_value > 5:
                st.markdown("👍 **Good yield potential.** Consider minor adjustments for optimization.")
            elif yield_value > 3:
                st.markdown("🔍 **Moderate yield potential.** Review your farming practices for improvements.")
            else:
                st.markdown("⚠️ **Below average yield potential.** Consider alternative crops or significant changes.")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Add timestamp to show when prediction was made
            st.caption(f"Prediction made on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            st.error(f"❌ Prediction failed: {str(e)}")
            st.info("Please ensure all inputs are valid and try again.")

# Add a footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.8rem;">
    Crop Yield Prediction Tool | Developed with Streamlit | Data-driven farming solutions
</div>
""", unsafe_allow_html=True)