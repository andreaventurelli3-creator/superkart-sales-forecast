
# Import necessary libraries
import numpy as np
import joblib                                   # to load the saved model
import pandas as pd
from flask import Flask, request, jsonify       # Flask web framework

# Create the Flask app
superkart_api = Flask("SuperKart")

# Load the trained model (pipeline = encoding + Random Forest)
model = joblib.load("superkart_model.joblib")

# The 10 features the model expects
FEATURES = [
    "Product_Weight", "Product_Sugar_Content", "Product_Allocated_Area",
    "Product_MRP", "Store_Size", "Store_Location_City_Type", "Store_Type",
    "Product_Id_char", "Store_Age_Years", "Product_Type_Category",
]

# Route 1: home page, used to check the API is running
@superkart_api.get("/")
def home():
    return "Welcome to the SuperKart System"

# Route 2: predict sales for a single product
@superkart_api.post("/v1/predict")
def predict_sales():
    try:
        data = request.get_json()
        sample = {feature: data[feature] for feature in FEATURES}
        input_data = pd.DataFrame([sample])
        prediction = model.predict(input_data).tolist()[0]
        return jsonify({"Sales": prediction})
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route 3: predict sales for a batch of products
@superkart_api.post("/v1/predictbatch")
def predict_sales_batch():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        input_data = pd.read_csv(request.files["file"])
        predictions = model.predict(input_data[FEATURES]).tolist()
        return {str(i): round(p, 2) for i, p in enumerate(predictions)}
    except KeyError as e:
        return jsonify({"error": f"Missing column: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Only used for local testing; in production Gunicorn runs the app
if __name__ == "__main__":
    superkart_api.run(debug=True)
