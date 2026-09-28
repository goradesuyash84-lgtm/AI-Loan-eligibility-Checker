# AI Loan Eligibility Checker

A simple student-friendly Flask web project with:
- Loan eligibility checker
- Credit score analyzer
- EMI calculator
- AI financial tips (optional Claude API)
- Responsive dark glassmorphism interface
- Ready for GitHub and Render

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

Open: http://127.0.0.1:5000

## Deploy on Render

1. Upload this folder to a GitHub repository.
2. In Render, choose New -> Web Service.
3. Select the GitHub repository.
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. Optional: add `ANTHROPIC_API_KEY` in Render Environment Variables to enable Claude AI tips.

This is an educational project. Loan eligibility is only a demo calculation and is not a real bank approval.
