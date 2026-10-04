
import sqlite3

def normalize_countries(countries):
    normalized = []
    for c in countries:
        iso = c.get("codes", {}).get("alpha_3")
        capitals = c.get("capitals", [])
        currencies = c.get("currencies", [])

        # Skip if missing critical fields
        if not iso or not capitals or not currencies:
            continue

        normalized.append({
            "name": c.get("names", {}).get("common"),
            "iso_alpha3": iso,
            "capital": capitals[0].get("name"),
            "population": c.get("population", 0),
            "region": c.get("region", "N/A"),
            "currency": currencies[0].get("code")
        })
    return normalized


def normalize_gdp(gdp_records):
    """
    Filter GDP records to latest year and flatten structure.
    """
    latest_year = max(int(r["date"]) for r in gdp_records if r.get("date").isdigit())
    normalized = []
    for r in gdp_records:
        if str(r.get("date")) == str(latest_year):
            normalized.append({
                "iso_alpha3": r.get("countryiso3code"),
                "gdp_per_capita": r.get("value")
            })
    return normalized


def merge_data(countries, gdp):
    """
    Merge countries and GDP by ISO Alpha-3 code.
    """
    gdp_map = {r["iso_alpha3"]: r["gdp_per_capita"] for r in gdp if r["iso_alpha3"]}
    merged = []
    for c in countries:
        iso = c["iso_alpha3"]
        c["gdp_per_capita"] = gdp_map.get(iso, None)
        merged.append(c)
    return merged


def load_to_sqlite(merged, db_path="countries.db"):
    """
    Load merged data into SQLite.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            name TEXT,
            iso_alpha3 TEXT PRIMARY KEY,
            capital TEXT,
            population INTEGER,
            region TEXT,
            currency TEXT,
            gdp_per_capita REAL
        )
    """)

    # Insert data
    for c in merged:
        cur.execute("""
            INSERT OR REPLACE INTO countries 
            (name, iso_alpha3, capital, population, region, currency, gdp_per_capita)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            c["name"], c["iso_alpha3"], c["capital"], c["population"],
            c["region"], c["currency"], c["gdp_per_capita"]
        ))

    conn.commit()
    conn.close()
    print(f"Loaded {len(merged)} records into SQLite.")


if __name__ == "__main__":
    # Import extract functions
    from extract import fetch_all_countries, fetch_worldbank_gdp_per_capita

    countries_raw = fetch_all_countries()
    gdp_raw = fetch_worldbank_gdp_per_capita()

    countries = normalize_countries(countries_raw)
    gdp = normalize_gdp(gdp_raw)
    merged = merge_data(countries, gdp)

    load_to_sqlite(merged)
