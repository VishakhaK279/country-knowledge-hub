import streamlit as st
import httpx
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("RESTCOUNTRIES_API_KEY")
headers = {"Authorization": f"Bearer {API_KEY}"}

st.title("🌍 Country Knowledge Hub")

# Fetch country list once and cache it
@st.cache_data
def get_country_list():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    base_url = "https://api.restcountries.com/countries/v5?response_fields=names.common"
    countries = []
    offset = 0
    limit = 100

    with httpx.Client() as client:
        while True:
            url = f"{base_url}&limit={limit}&offset={offset}"
            r = client.get(url, headers=headers)
            r.raise_for_status()
            payload = r.json()
            objects = payload.get("data", {}).get("objects", [])
            countries.extend([obj["names"]["common"] for obj in objects])
            meta = payload.get("data", {}).get("meta", {})
            print(f"Fetched {meta.get('count')} countries at offset {offset}")

            if not meta.get("more", False):
                break
            offset += limit

    return sorted(countries)



countries = get_country_list()

st.write(f"Loaded {len(countries)} countries")



selected_country = st.selectbox("Choose a country:", countries)
#country = st.text_input("Enter a country name:")

if st.button("Get Info"):
    with httpx.Client() as client:
        r = client.post("http://localhost:8000/country", json={"country_name": selected_country})
        if r.status_code == 200:
            data = r.json()
            st.write(f"**Name:** {data['country_name']}")
            st.write(f"**Capital:** {data['capital']}")
            st.write(f"**Population:** {data['population']:,}")
            st.write(f"**Region:** {data['region']}")
            st.write(f"**Currency:** {data['currency']}")
        else:
            error_message = r.json().get("detail", "Unknown error")
            st.error(f"Error: {error_message}")
