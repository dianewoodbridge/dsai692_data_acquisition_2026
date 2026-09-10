from fastapi import HTTPException
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


class ItemDetaliResponse(BaseModel):
    name: str
    price: float


@app.get("/item_details/{item_name}", response_model=ItemDetaliResponse)
def return_item_details(item_name: str):
    if (item_name not in items.keys()):
        raise HTTPException(
            status_code=404,
            detail=f"Item, {item_name} not found")

    return {"name": items[item_name].name,
            "price": items[item_name].price}
