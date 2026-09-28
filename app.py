import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def loan_check(data):
    age = int(data.get("age", 0))
    income = float(data.get("income", 0))
    credit = int(data.get("credit_score", 0))
    loan = float(data.get("loan_amount", 0))
    employment = data.get("employment", "Salaried")

    score = 0
    if 21 <= age <= 60: score += 20
    if income >= 30000: score += 25
    if credit >= 750: score += 30
    elif credit >= 650: score += 20
    elif credit >= 600: score += 10
    if loan <= income * 20: score += 15
    if employment in ["Salaried", "Self Employed"]: score += 10

    eligible = score >= 65

    if eligible:
        message = "Your profile looks suitable for a loan based on the entered details."
    else:
        message = "Your profile may need improvement before applying for this loan."

    return {"eligible": eligible, "score": score, "message": message}

@app.route("/")
def home():
    return render_template("index.html")

@app.post("/api/check-loan")
def check_loan():
    try:
        return jsonify(loan_check(request.get_json(force=True)))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.post("/api/emi")
def emi():
    try:
        data = request.get_json(force=True)
        principal = float(data["amount"])
        annual_rate = float(data["rate"])
        years = float(data["years"])
        monthly_rate = annual_rate / 12 / 100
        months = years * 12

        if monthly_rate == 0:
            value = principal / months
        else:
            value = principal * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)

        total = value * months
        return jsonify({"emi": round(value, 2), "total": round(total, 2),
                        "interest": round(total - principal, 2)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.get("/api/credit/<int:score>")
def credit(score):
    if score >= 750:
        category, tip = "Excellent", "Maintain timely payments and low credit utilization."
    elif score >= 700:
        category, tip = "Good", "Keep payments on time and avoid unnecessary new credit."
    elif score >= 650:
        category, tip = "Fair", "Try to reduce outstanding balances and maintain timely payments."
    else:
        category, tip = "Needs Improvement", "Focus on timely payments and reducing outstanding debt."
    return jsonify({"score": score, "category": category, "tip": tip})

@app.post("/api/ai-tips")
def ai_tips():
    # Optional Claude integration. Add ANTHROPIC_API_KEY in Render to enable it.
    question = request.get_json(force=True).get("question", "").strip()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        return jsonify({
            "answer": "For general guidance: maintain timely payments, keep credit-card utilization low, compare loan interest rates, and borrow only what you can comfortably repay. This demo does not provide personalized financial advice."
        })

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model="claude-3-5-haiku-latest",
            max_tokens=300,
            system="Give short, general financial education. Do not claim to approve loans or provide regulated financial advice.",
            messages=[{"role": "user", "content": question or "Give three simple tips for improving loan readiness."}]
        )
        return jsonify({"answer": msg.content[0].text})
    except Exception as e:
        return jsonify({"answer": "AI service is not configured. Basic tip: keep payments on time, reduce outstanding debt, and compare loan terms before applying."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
