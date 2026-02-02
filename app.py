

from flask import Flask, render_template, request, redirect
import pickle
import logging

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 86400

model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return redirect("/")

    iq = float(request.form["iq"])
    cgpa = float(request.form["cgpa"])
    company = request.form["company"]

    if company == "service":
        min_iq, min_cgpa = 75, 6.5
    else:
        min_iq, min_cgpa = 90, 8.0

    if iq < min_iq or cgpa < min_cgpa:
        return render_template(
            "index.html",
            prediction_text="Not Eligible ❌ (Does not meet company criteria)"
        )

    prob = model.predict_proba([[iq, cgpa]])[0][1]

    if prob >= 0.7:
        result = "Placed ✅ (High confidence)"
    elif prob >= 0.4:
        result = "Borderline ⚠️ (Interview dependent)"
    else:
        result = "Not Eligible ❌"

    return render_template("index.html", prediction_text=result)
