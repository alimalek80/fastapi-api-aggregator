import time
import asyncio
import requests
import httpx
from fastapi import FastAPI

app = FastAPI()

EXTERNAL_URLS = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
]


@app.get("/sync")
def sync_benchmark():
    start = time.perf_counter()

    results = []
    for url in EXTERNAL_URLS:
        response = requests.get(url)
        results.append(response.status_code)

    elapsed = time.perf_counter() - start

    return {
        "mode": "sync",
        "requests_made": len(EXTERNAL_URLS),
        "status_codes": results,
        "elapsed_seconds": round(elapsed, 2),
    }


@app.get("/async")
async def async_benchmark():
    start = time.perf_counter()

    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in EXTERNAL_URLS]
        responses = await asyncio.gather(*tasks)

    elapsed = time.perf_counter() - start

    return {
        "mode": "async",
        "requests_made": len(EXTERNAL_URLS),
        "status_codes": [r.status_code for r in responses],
        "elapsed_seconds": round(elapsed, 2),
    }