from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    iq = float(request.form["iq"])
    cgpa = float(request.form["cgpa"])
    company = request.form["company"]

    # Company-wise eligibility rules
    if company == "service":
        min_iq = 75
        min_cgpa = 6.5
    else:  # product-based
        min_iq = 90
        min_cgpa = 8.0

    # Hard eligibility check
    if iq < min_iq or cgpa < min_cgpa:
        return render_template(
            "index.html",
            prediction_text="Not Eligible ❌ (Does not meet company criteria)"
        )

    # Logistic Regression probability
    prob = model.predict_proba([[iq, cgpa]])[0][1]

    # Final decision
    if prob >= 0.7:
        result = "Placed ✅ (High confidence)"
    elif prob >= 0.4:
        result = "Borderline ⚠️ (Interview dependent)"
    else:
        result = "Not Eligible ❌"

    return render_template("index.html", prediction_text=result)


if __name__ == "__main__":
    app.run(debug=True)
