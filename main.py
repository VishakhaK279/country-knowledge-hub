from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("RESTCOUNTRIES_API_KEY")

app = FastAPI(title="Country Knowledge Hub")

class CountryRequest(BaseModel):
    country_name: str

class CountryResponse(BaseModel):
    country_name: str
    capital: str
    population: int
    region: str
    currency: str

headers = {"Authorization": f"Bearer {API_KEY}"}

@app.post("/country", response_model=CountryResponse)
async def get_country_info(req: CountryRequest):
    async with httpx.AsyncClient() as client:
        try:
            # v5 endpoint: names.common
            url = f"https://api.restcountries.com/countries/v5/names.common/{req.country_name}"
            r = await client.get(url, headers=headers)
            r.raise_for_status()
            payload = r.json()

            objects = payload.get("data", {}).get("objects", [])
            if not objects:
                raise HTTPException(status_code=404, detail="Country not found")

            country = next(
                (obj for obj in objects if obj.get("names", {}).get("common", "").lower() == req.country_name.lower()),
                None
            )
            if not country:
                raise HTTPException(status_code=404, detail="Exact country not found")
            
            return CountryResponse(
                country_name=country.get("names", {}).get("common", "N/A"),
                capital=country.get("capital", ["N/A"])[0],
                population=country.get("population", 0),
                region=country.get("region", "N/A"),
                currency=country.get("currencies", [{"code": "N/A"}])[0]["code"]
            )
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=404, detail="Country not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
