# 🌍 Country Knowledge Hub

A Streamlit web app that lets you explore information about countries worldwide.  
Built with **Python, Streamlit, and REST Countries API v5**.

---

## ✨ Features
- Fetches live country data using REST Countries API.
- Handles **API pagination** (solves the 100‑record limit).
- Displays country details: Name, Capital, Population, Region, Currency.
- Clean dark‑theme UI with dropdown selection.

---

## 🚀 How to Run
1. Clone the repo:
   ```bash
   git clone https://github.com/<your-username>/country-knowledge-hub.git
   cd country-knowledge-hub```
   
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
  
3. Add your REST Countries API key to a .env file:
   ```code
    RESTCOUNTRIES_API_KEY=your_api_key_here

5. Run the app:
   ```bash
   streamlit run app.py

## 🛠️ Tech Stack
Streamlit for UI
httpx for API calls
dotenv for environment variables
REST Countries API v5


