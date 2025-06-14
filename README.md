# Real-Time Phishing URL Detection Chrome Extension

## Introduction

Hi! This is a Chrome Extension we helped build as part of a final project to fight one of the biggest cybersecurity threats today: phishing. We used machine learning (specifically, a Random Forest Classifier) to detect suspicious URLs in real-time and warn users before they get tricked.

Our goal was to make something lightweight, fast, and understandable—especially for non-technical users—without compromising security or privacy.

---

## Problem

Phishing attacks are responsible for millions of dollars in damages each year. Most detection systems rely on blacklists, which don’t catch new threats quickly enough. On top of that, many ML solutions are hard to understand and even harder to deploy.

So we asked ourselves:  
**Can we build a user-friendly browser extension that uses machine learning to detect phishing URLs in real time—without invading anyone’s privacy?**

---

## Our Solution

We created a Chrome Extension that:

- Analyzes the current tab’s URL when the user clicks a button.
- Sends it to a Flask backend where a trained ML model predicts its phishing risk.
- Shows the user a color-coded risk level: Green (Low), Yellow (Medium), Red (High).
- Uses **no personal data**, stores **nothing**, and works **locally**.

---

### Dataset

- We used a labeled dataset from Mendeley with over **450,000 URLs**.
- Only **23% were phishing**, so we had to handle class imbalance carefully.
- No oversampling—we adjusted model thresholds instead.

### Model

- We trained a **Random Forest Classifier** with:
  - 100 estimators
  - Custom threshold = 0.3 (to catch more phishing URLs)
- Accuracy = **92.03%**
- Precision (phishing) = **89%**
- Recall (phishing) = **76%**
- F1 Score = **0.82**

### Features Used

Here are some of the handcrafted features we extracted from URLs:

- IP address instead of domain
- Use of shortening services (bit.ly, etc.)
- Suspicious symbols (like `@`, extra `//`)
- Keyword patterns (e.g., "login", "verify")
- Subdomain depth
- Whether it ends in `.exe`
- And many more!

### Chrome Extension

Built with:

- `manifest.json`: Permissions & setup
- `popup.html`: Clean UI
- `popup.js`: Captures URL and calls backend
- Color-coded results + phishing confidence bar

### Backend (Flask API)

- Exposes a `/check` POST endpoint
- Loads the trained model and processes the URL
- Extracts features in real time
- Returns prediction + risk score to the extension
- Deployed locally for this project (cloud deployment = future work!)

---

## Security and Privacy

We designed this with security in mind:

- No user data stored or tracked.
- Minimal permissions (only current tab).
- Secure API communication with CORS enabled.
- No external database or cookie access.
- Compliant with Chrome Web Store policies.

---

## Testing & Evaluation

We tested:

- Individual features with mock URLs
- Backend API with malicious and clean URLs
- Full integration from URL click ➝ backend ➝ Chrome UI
- Network failure handling (with graceful error messages)

---

##  Model Insights

- Most important features:
  - Subdomain depth
  - Number of special characters
  - Digits in the URL
  - Suspicious keywords
- We chose a **lower threshold (0.3)** to prioritize **security** (better to warn too often than miss real threats!).

---

## Future Improvements

- Deploy backend to cloud (Heroku, Render, etc.)
-  Add HTTPS encryption for API
- Make it work on Firefox and Edge
- Expand analysis to HTML/JS content (not just URLs)
- Add user feedback system (Was this a false alarm?)

## 📚 References

We used and cited research, public datasets, and development documentation from:

- IBM Security Reports
- Mendeley Data (Phishing Dataset)
- Google Chrome Extension Docs
- Flask and Scikit-learn Libraries
- GeeksforGeeks (Handling imbalanced datasets)
- MDN Web Docs (CORS)

## Lessons Learned

We learned a lot about:

- Real-world phishing techniques
- Balancing ML performance with usability
- The challenges of browser extension security
- Debugging end-to-end systems across frontend and backend

We hope this project contributes to safer browsing for everyone!

