# FastAPI API Aggregator

The FastAPI counterpart to [async-api-aggregator](https://github.com/alimalek80/async-api-aggregator), built to compare an async-first framework against Django's async workaround, using the exact same benchmark.

## The experiment

Same 5 external URLs (`httpbin.org/delay/1`, each artificially delayed by 1 second), same idea: call them one after another versus all at once.

| Endpoint | Method | Result |
|---|---|---|
| `GET /sync` | One request after another (`requests`) | **7.92 seconds** |
| `GET /async` | All requests concurrently (`httpx` + `asyncio.gather`) | **1.6 seconds** |

That's roughly a **5x speedup**.

## Django vs FastAPI, side by side

In the previous project, [async-api-aggregator](https://github.com/alimalek80/async-api-aggregator), the same benchmark was built with Django and DRF. The comparison between the two is as follows:

| | Django/DRF | FastAPI |
|---|---|---|
| Sync | 8.57s | 7.92s |
| Async | 2.62s | **1.6s** |
| Speedup | 3.3x | **4.95x** |

Both use the exact same async tools underneath: `httpx.AsyncClient` and `asyncio.gather`. The difference is what happens around them.

## Why FastAPI's async endpoint is faster

Django REST Framework does not yet fully support async views. To make the async endpoint work in the Django version, a plain Django function-based view had to be used instead of DRF's `APIView`, and that path still carries extra sync/async bridging overhead under the hood.

FastAPI was built async-first from day one. A sync endpoint (`def`) and an async endpoint (`async def`) can sit side by side in the same file, no workaround needed, and the async path has no extra bridging layer to cross. That's the concrete, measured reason it comes out faster here, not just a framework preference.

## Project structure

```
fastapi-api-aggregator/
├── main.py            # FastAPI app with both endpoints
└── requirements.txt
```

## Running it locally

```bash
git clone https://github.com/alimalek80/fastapi-api-aggregator.git
cd fastapi-api-aggregator

python -m venv venv
venv\Scripts\Activate.ps1        # Windows PowerShell
# source venv/bin/activate       # macOS/Linux

pip install -r requirements.txt

uvicorn main:app --reload
```

Then compare the two endpoints:

```
http://127.0.0.1:8000/sync
http://127.0.0.1:8000/async
```

## Stack

- FastAPI
- Uvicorn (ASGI server)
- httpx (async HTTP client)
- requests (sync HTTP client)

## Related

- [async-api-aggregator](https://github.com/alimalek80/async-api-aggregator) — the original Django/DRF version of this same benchmark.