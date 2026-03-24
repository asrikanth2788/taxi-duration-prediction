import joblib
import json
from flask import Flask, request, jsonify

def load_model():
    dv, model = joblib.load('./models/linear_model.joblib')
    return dv, model

def prepare_data(ride):
    features = {}
    features["DO_PU"] = str(ride["DOLocationID"]) + "_" + str(ride["PULocationID"])
    features["trip_distance"] = ride["trip_distance"]
    return features

app = Flask("taxi-duration-prediction")

@app.route("/predict", methods=["POST"])
def predict():
    ride = request.get_json()
    dv, model = load_model()
    features = prepare_data(ride)
    X_val = dv.transform(features)
    return jsonify(f"{model.predict(X_val)[0]:.2f}")

@app.route("/predict", methods=["GET"])
def predict_via_get():
    args = request.args
    
    ride = {
        "PULocationID": int(args.get("PULocationID")),
        "DOLocationID": int(args.get("DOLocationID")),
        "trip_distance": float(args.get("trip_distance"))
    }
   
    dv, model = load_model()
    features = prepare_data(ride)
    X_val = dv.transform(features)
    return jsonify(f"{model.predict(X_val)[0]:.2f}")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9696)