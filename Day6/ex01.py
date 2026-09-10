
from fastapi import FastAPI

# 1. Create a FastAPI App Instance
app = FastAPI()

# 2. Define a function and associate with a route.


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item_w_path_param(item_id: int):
    return {"item_id": item_id}


@app.get("/items/")
def read_item_w_query_param(item_id: int | None = None, ct: int = 0):
    return {"item_id": item_id, "count": ct}


@app.get("/name")
def return_name(name: str):
    return {"name": name}
