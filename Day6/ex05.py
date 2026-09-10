import asyncio
import time
import httpx
from fastapi import FastAPI

app = FastAPI()

url = "https://httpbin.org/delay/1.2"  # send a response after 1.2 sec


@app.get("/sync")
def sync_call():
    response1 = httpx.get(url)
    response2 = httpx.get(url)
    return {"first": response1.json(),
            "second": response2.json()}


@app.get("/async")
async def async_call():
    async with httpx.AsyncClient() as client:
        response1 = await client.get(url)
        response2 = await client.get(url)
    return {"first": response1.json(),
            "second": response2.json()}
