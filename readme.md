# 🌾 Crop Yield Prediction App

A Streamlit web application that predicts crop yields based on environmental and agricultural factors using machine learning.

## Overview

This application helps farmers and agricultural professionals estimate crop yields by analyzing key factors such as soil type, rainfall, temperature, and farming practices. The predictions are based on a trained machine learning model that processes these inputs to generate yield estimates in tons per hectare.

## Features

- **User-friendly Interface**: Clean, intuitive design for easy data input
- **Comprehensive Inputs**: Capture all relevant agricultural factors 
- **Real-time Predictions**: Instant yield estimates upon form submission
- **Interpretive Results**: Contextual feedback on yield potential
- **Educational Content**: Farming tips and optimal growing conditions

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/crop-yield-prediction.git

   cd crop-yield-prediction
   ```

2. Create a virtual environment (recommended):
   ```
   python -m venv venv

   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Required Packages

Create a `requirements.txt` file with the following content:

```
streamlit==1.27.0
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
```

## Usage

1. Ensure you have the trained model file (`model.pkl`) in the same directory as the application.

2. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

3. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501).

4. Fill in the form with your specific agricultural data and click "Predict Yield" to get results.
