# 🌍 Country Knowledge Hub

A Python + Streamlit project that started as a simple country explorer and has now grown into a **full ETL pipeline** with SQLite integration.  
Built with **Python, Streamlit, REST Countries API v5, World Bank API, and SQLite**.

---

## ✨ Features
- **Streamlit UI**
  - Fetches live country data using REST Countries API.
  - Handles API pagination (solves the 100‑record limit).
  - Displays country details: Name, Capital, Population, Region, Currency.
  - Clean dark‑theme UI with dropdown selection.

- **ETL Pipeline**
  - Extracts country metadata + GDP per capita data.
  - Transforms and merges datasets on ISO Alpha‑3.
  - Loads ~245 clean records into SQLite (`countries.db`).
  - Validated against World Bank data (India’s GDP per capita 2025 matches).

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

6. ETL Pipeline:
   ```bash
   python extract.py
   python transform.py

## 🛠️ Tech Stack
Streamlit for UI
httpx for API calls
dotenv for environment variables
SQLite for local database storage
REST Countries API v5 + World Bank API



