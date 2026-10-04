import os
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("RESTCOUNTRIES_API_KEY")
headers = {"Authorization": f"Bearer {API_KEY}"}

def fetch_all_countries():
    """
    Fetch all countries from REST Countries v5 API using pagination.
    Returns a list of country objects.
    """
    base_url = "https://api.restcountries.com/countries/v5"
    countries = []
    offset = 0
    limit = 100

    while True:
        url = f"{base_url}?limit={limit}&offset={offset}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        payload = response.json()

        objects = payload.get("data", {}).get("objects", [])
        countries.extend(objects)

        meta = payload.get("data", {}).get("meta", {})
        print(f"Fetched {meta.get('count')} countries at offset {offset}")

        if not meta.get("more", False):
            break
        offset += limit

    return countries

def fetch_worldbank_gdp_per_capita():
    """
    Fetch GDP per capita for all countries from World Bank API.
    Indicator: NY.GDP.PCAP.CD (GDP per capita, current US$)
    """
    url = "http://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.CD?format=json&per_page=20000"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data[1]  # second element has actual records

'''if __name__ == "__main__":
    # Validate REST Countries
    countries = fetch_all_countries()
    print(f"Total countries fetched: {len(countries)}")
    if countries:
        sample = countries[0]
        print("Sample country:", sample.get("names", {}).get("common"))
        print("ISO Alpha-3:", sample.get("codes", {}).get("alpha3"))
        print("Capital:", sample.get("capital", ["N/A"])[0])
        print("Population:", sample.get("population", 0))
        print("Region:", sample.get("region", "N/A"))

    # Validate World Bank GDP
    gdp_records = fetch_worldbank_gdp_per_capita()
    print(f"\nTotal GDP records fetched: {len(gdp_records)}")
    if gdp_records:
        sample_gdp = gdp_records[0]
        print("Sample GDP record:", sample_gdp)'''
