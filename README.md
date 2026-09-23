# PhishXplain

### AI × Cybersecurity | Team Glass

PhishXplain is an explainable phishing detection MVP developed by **TEAM GLASS** for the AI × Cybersecurity hackathon.

The project analyzes either:

- Suspicious URLs
- Suspicious messages

and produces:

- Risk score (0–100)
- Risk classification
- Reasons/evidence behind the score
- Recommended safety action

The core product idea is:

> **Detect → Explain → Protect**

---

## Team

**TEAM GLASS**

Project: **PhishXplain — Explainable AI for Phishing Link & Message Detection**

---

## Problem Statement

Phishing attacks commonly use malicious links and deceptive messages to trick users into:

- Revealing passwords or OTPs
- Sharing banking/payment information
- Visiting fake login pages
- Taking urgent or unauthorized actions
- Trusting impersonated organizations

Traditional detection tools may simply label something as phishing without clearly explaining the reasons.

PhishXplain focuses on an understandable analysis experience that shows **why an input may be suspicious** and what the user should do next.

---

## Current Solution

PhishXplain accepts two types of input:

### 1. URL Analysis

The URL analyzer currently checks multiple cybersecurity indicators, including:

- HTTPS usage
- IP address instead of a domain
- Unusually long URLs
- Multiple subdomains
- `@` symbol
- Suspicious encoded/special characters
- Suspicious keywords such as:
  - login
  - verify
  - account
  - password
  - bank
  - payment
  - secure
  - update
- URL shorteners
- Hyphens in domains
- Deceptive/multi-level domain structures
- Sensitive query parameters such as:
  - login
  - password
  - verify
  - account
  - token
  - session

### 2. Message Analysis

The message analyzer currently checks:

- Urgency language
- Account blocking/suspension language
- Credential requests
- OTP/password/PIN/CVV requests
- URLs inside messages
- Payment/financial requests
- Impersonation indicators
- Excessive capitalization
- Excessive exclamation marks

---

## Risk Classification

The current rule-based engine uses the following thresholds:

| Score | Classification |
|---:|---|
| 0–39 | LOW RISK |
| 40–69 | SUSPICIOUS |
| 70–100 | HIGH RISK |

The score is capped at 100.

The system also generates a recommendation based on the detected risk level.

---

## AI Integration

A pretrained Hugging Face phishing detection model has been added as the planned AI component:

`cybersectony/phishing-email-detection-distilbert_v2.4.1`

The AI integration is designed to work alongside the existing cybersecurity rules instead of replacing them.

Conceptually:

```text
                 USER INPUT
                     │
          ┌──────────┴──────────┐
          │                     │
      URL Analysis        Message Analysis
          │                     │
          └──────────┬──────────┘
                     │
              Cybersecurity Rules
                     │
                     +
                AI Analysis
                     │
                Risk Engine
                     │
          ┌──────────┼──────────┐
          │          │          │
      Risk Score  Reasons  Recommendation
```

The AI component is intended to provide additional phishing-related evidence while the existing rule-based analyzer remains the core fallback.

### Current AI status

The AI dependencies have been installed:

```text
transformers
torch
```

The AI model integration has been started, but it is still being tested and debugged.

**Important:** the rule-based analyzer should remain functional even if the AI model is unavailable.

---

## Technology Stack

### Frontend

- HTML5
- CSS3
- JavaScript

The frontend provides:

- URL Analysis mode
- Message Analysis mode
- Input area
- Character counter
- Analyze Threat button
- Loading indicator
- Risk score display
- Classification badge
- Suspicion reasons
- Safety recommendation
- PhishXplain / TEAM GLASS branding

### Backend

- Python
- FastAPI
- Uvicorn

### AI / ML

- Hugging Face Transformers
- PyTorch
- Pretrained phishing detection model

### Cybersecurity Logic

Custom rule-based phishing indicators implemented in Python.

---

## Project Structure

```text
PhishXplain/
│
├── backend/
│   │
│   ├── main.py
│   ├── analyzer.py
│   ├── ai_model.py
│   └── requirements.txt
│
└── frontend/
    │
    ├── index.html
    ├── style.css
    └── script.js
```

Depending on the local project setup, the backend and frontend may be located inside the same project directory.

---

## Backend API

### Endpoint

```http
POST /analyze
```

### Request

```json
{
  "type": "url",
  "input": "https://example.com/login"
}
```

or:

```json
{
  "type": "message",
  "input": "Your account will be blocked. Verify immediately."
}
```

### Response

The frontend expects a response containing:

```json
{
  "score": 75,
  "classification": "HIGH RISK",
  "reasons": [
    "Suspicious keyword detected: login",
    "URL does not use HTTPS"
  ],
  "recommendation": "Do not open this URL or enter personal information."
}
```

---

## Running the Project

### 1. Install dependencies

From the backend/project directory:

```bash
pip install -r requirements.txt
```

If AI dependencies are not already included:

```bash
pip install transformers torch
```

### 2. Start FastAPI

```bash
uvicorn main:app --reload
```

The application should be available at:

```text
http://127.0.0.1:8000
```

### 3. Open the application

Open:

```text
http://127.0.0.1:8000/
```

The FastAPI backend serves the frontend.

---

## Frontend → Backend Flow

The current frontend sends the selected analysis type and user input to:

```text
POST http://127.0.0.1:8000/analyze
```

The request format is:

```json
{
  "type": "url",
  "input": "USER INPUT"
}
```

The backend processes the input and returns the analysis result.

The frontend then displays:

```text
Risk Score
     ↓
Classification
     ↓
Why is it suspicious?
     ↓
Recommended Action
```

---

## Example Inputs for Demo

### Suspicious URL

```text
http://secure-login-account-verify.example.com/login
```

### Suspicious Message

```text
URGENT! Your bank account has been suspended.
Verify your account immediately or it will be permanently blocked.
```

### Another phishing-style message

```text
Congratulations! You have won a reward.
Pay the processing fee now to receive your prize.
```

### Legitimate-style example

```text
Your order has been delivered successfully.
Thank you for shopping with us.
```

These examples are intended for safe demonstration and testing.

---

## Explainable Output

The project does not only return a classification.

It explains the detected indicators, for example:

```text
HIGH RISK

Why is it suspicious?

✓ Urgency indicator detected
✓ Sensitive information request detected
✓ Message contains a clickable URL
✓ Message may be impersonating a trusted organization

Recommended Action:

Do not click links or provide passwords, OTPs,
payment details, or other sensitive information.
```

This supports the project's main differentiator:

> **Don't just detect phishing — explain the evidence.**

---

## Safety & Privacy

PhishXplain is designed as a cybersecurity analysis MVP.

Do not enter real:

- Passwords
- OTPs
- Credit/debit card numbers
- Banking credentials
- API keys
- Personal authentication information

Use simulated/demo data during development and the hackathon presentation.

The application provides **risk indicators**, not guaranteed security verdicts.

---

## Current Development Status

### Completed

- [x] PhishXplain project concept
- [x] TEAM GLASS branding
- [x] HTML frontend
- [x] CSS interface
- [x] URL Analysis mode
- [x] Message Analysis mode
- [x] FastAPI backend
- [x] `/analyze` API endpoint
- [x] Rule-based URL analysis
- [x] Rule-based message analysis
- [x] Risk scoring
- [x] Risk classification
- [x] Explainable reasons
- [x] Safety recommendations
- [x] Frontend result rendering
- [x] Transformers and PyTorch installation
- [x] Initial pretrained AI model integration

### In Progress

- [ ] Complete AI model integration
- [ ] Validate AI predictions against demo examples
- [ ] Tune AI + cybersecurity score combination
- [ ] Complete end-to-end AI-powered demo
- [ ] Final testing before presentation

---

## Known Development Issue

During AI integration, a backend error occurred because the URL analysis function accidentally called:

```python
self.run_ai_analysis(message)
```

instead of:

```python
self.run_ai_analysis(url)
```

The correct variable inside `analyze_url()` is `url`.

The message analyzer should use:

```python
self.run_ai_analysis(message)
```

This issue is being fixed during integration testing.

---

## MVP Architecture

```text
┌──────────────────────────────┐
│          FRONTEND            │
│      HTML + CSS + JS         │
│                              │
│  URL Analysis                │
│  Message Analysis            │
└──────────────┬───────────────┘
               │
               │ HTTP POST
               ▼
┌──────────────────────────────┐
│          FASTAPI             │
│          main.py             │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        PHISH ANALYZER        │
│        analyzer.py           │
│                              │
│  URL Rules                   │
│  Message Rules               │
│  AI Analysis                 │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         RISK ENGINE          │
│                              │
│     Risk Score 0–100         │
│     Classification           │
│     Evidence                 │
│     Recommendation            │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       EXPLAINABLE RESULT     │
│                              │
│   DETECT → EXPLAIN → PROTECT │
└──────────────────────────────┘
```

---

## Hackathon Demo Flow

For the final demo, the recommended flow is:

### 1. Start with the problem

Show a suspicious phishing message or URL.

### 2. Submit the input

Use the PhishXplain interface.

### 3. Analyze

The backend checks cybersecurity indicators and AI signals.

### 4. Show the risk score

Example:

```text
Risk Score: 86 / 100
HIGH RISK
```

### 5. Explain the evidence

Show the individual reasons detected.

### 6. Show the recommended action

Explain what the user should do to stay safe.

### 7. Demonstrate a second input

Use a normal/legitimate-style example to demonstrate that the system can produce a different risk assessment.

---

## Project Vision

PhishXplain aims to make phishing detection more understandable to everyday users.

Instead of only saying:

```text
PHISHING
```

the system aims to communicate:

```text
HIGH RISK

Why?

• Urgency detected
• Credential request detected
• Suspicious URL detected
• AI detected phishing-like patterns

What should you do?

Do not click or share sensitive information.
Verify the sender through an official channel.
```

---

## Team

### TEAM GLASS

**PhishXplain**

> Detect. Explain. Protect.
