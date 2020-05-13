from fastapi import FastAPI
from starlette import responses
from prometheus_client import Counter, generate_latest

app = FastAPI()


REQUEST_COUNTER = Counter("demo_app_request_count", "Demo app HTTP request count")


@app.get("/")
def read_root():
    REQUEST_COUNTER.inc()
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/metrics")
def metrics():
    return responses.Response(generate_latest(), 200)
