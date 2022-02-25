from fastapi import APIRouter

from ..models.item import Item

router = APIRouter(tags=["items"])


@router.get("/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@router.post("/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@router.put("/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}
