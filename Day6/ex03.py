from fastapi import FastAPI
from pydantic import BaseModel


# 1. Create a FastAPI App Instance
app = FastAPI()
items = {}  # In-memory database


class Item(BaseModel):
    # 3. Define Pydantic Model
    name: str
    price: float
    instock_qt: int


class ItemResponse(BaseModel):
    total_worth: float


@app.post("/add_items/", response_model=ItemResponse)
def create_item(item: Item):
    # 2. Define a function and associate with a route.
    items[item.name] = item
    return {"message": "Item added successfully",
            "total_worth": item.price * item.instock_qt,
            "items": items}
