import joblib
from flask import Flask, request, jsonify

MODEL_PATH = "./models/linear_model.joblib"

def load_model(path: str = MODEL_PATH):
    return joblib.load(path)

def prepare_data(ride: dict) -> dict:
    return {
        "DO_PU": f'{ride["DOLocationID"]}_{ride["PULocationID"]}',
        "trip_distance": ride["trip_distance"],
    }

def parse_ride(req) -> dict:
    if req.method == "GET":
        payload = req.args
    else:
        payload = req.get_json(silent=True) or {}

    required = ["PULocationID", "DOLocationID", "trip_distance"]
    missing = [k for k in required if payload.get(k) is None]
    if missing:
        raise ValueError(f"Missing fields: {', '.join(missing)}")

    try:
        return {
            "PULocationID": int(payload.get("PULocationID")),
            "DOLocationID": int(payload.get("DOLocationID")),
            "trip_distance": float(payload.get("trip_distance")),
        }
    except (TypeError, ValueError):
        raise ValueError("Invalid field types. Expected int, int, float.")

app = Flask(__name__)
dv, model = load_model()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/predict", methods=["GET", "POST"])
def predict():
    try:
        ride = parse_ride(request)
        features = prepare_data(ride)
        X_val = dv.transform([features])  # single-row batch
        pred = float(model.predict(X_val)[0])
        return jsonify({"predicted_duration": round(pred, 2)})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9696)