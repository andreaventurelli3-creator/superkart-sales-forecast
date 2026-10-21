
import streamlit as st
import pandas as pd
import requests

# Address of the Flask backend. "backend" is the container name on the Docker network.
BACKEND_URL = "http://backend:7860"

st.title("SuperKart Sales Forecast")
st.write("Enter the product and store details below to predict the total sales.")

# ---- Single prediction: input fields ----
Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Allocated_Area = st.number_input("Product Allocated Area", min_value=0.0, value=0.027)
Product_MRP = st.number_input("Product MRP", min_value=0.0, value=117.08)
Store_Size = st.selectbox("Store Size", ["Small", "Medium", "High"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2",
                                         "Departmental Store", "Food Mart"])
Product_Id_char = st.selectbox("Product ID Prefix", ["FD", "DR", "NC"])
Store_Age_Years = st.number_input("Store Age (Years)", min_value=0, value=16)
Product_Type_Category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

# Build the JSON payload the API expects
product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type_Category": Product_Type_Category,
}

# Single prediction
if st.button("Predict", type="primary"):
    try:
        response = requests.post(f"{BACKEND_URL}/v1/predict", json=product_data)
        if response.status_code == 200:
            predicted_sales = response.json()["Sales"]
            st.success(f"Predicted Product Store Sales Total: {predicted_sales:.2f}")
        else:
            st.error(f"API error: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to the prediction API.")

# ---- Batch prediction ----
st.subheader("Batch Prediction")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    if st.button("Predict for Batch", type="primary"):
        try:
            response = requests.post(f"{BACKEND_URL}/v1/predictbatch",
                                     files={"file": uploaded_file})
            if response.status_code == 200:
                results = pd.DataFrame(list(response.json().items()),
                                       columns=["Row", "Predicted Sales"])
                st.success("Predictions completed successfully!")
                st.dataframe(results, use_container_width=True)
                st.download_button("Download predictions",
                                   results.to_csv(index=False),
                                   "predictions.csv", "text/csv")
            else:
                st.error(f"API error: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Unable to connect to the prediction API.")
