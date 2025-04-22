"""
API route definitions
"""

from fastapi import APIRouter, Depends
from fastapi import Header
from pydantic import BaseModel

from typing import Annotated

from app.config import get_firebase_user_from_token

router = APIRouter()


# get hello world
@router.get("/")
def read_root():
    """
    Get root, and respond with ` {"Hello": "World"}`
    """
    return {"Hello": "World"}


# get with Path Parameters
@router.get("/greet/{name}")
def greet(name: str):
    """Get Items

    Args:
        name (str): url path parameter

    Returns:
        json: key:"hello", value: "world"
    """
    return f"Hello {name}"


# get with Query Parameters
@router.get("/items/")
def read_parameters(category: str, brand: str):
    """read query paraemters, key=value pairs in the url string

    Args:
        category (str): category query parameter
        brand (str): brand query paraemter

    Returns:
        dict: keys category and brand
    """
    return {"category": category, "brand": brand}


# Post with Pydantic Body/Data Model
class ItemPost(BaseModel):
    """Post Body/Data Model

    Args:
        BaseModel (BaeModel): Pydantic Base Model
    """

    name: str
    description: str = None
    price: float
    tax: float = None


@router.post("/items_post/")
def create_item(item: ItemPost):
    """Create item from post
    Args:
        item (ItemPost): item following the ItemPost model

    Returns:
        ItemPost: returns the item
    """
    return item


# Get with Pydantic Return Model
class ItemGet(BaseModel):
    """Get Model

    Args:
        BaseModel (BaseModel): PyDantic Base Model
    """

    name: str
    description: str
    price: float


@router.get("/items_get/")
def read_items():
    """get items

    Returns:
        itemGet: itemGet type
    """
    items = [
        ItemGet(name="Foo", description="A new item", price=45.2),
        ItemGet(name="Bar", description="Another item", price=10.5),
    ]
    return items


# Authenticated Protected Route
@router.get("/protected")
# def protected(authorization: str):
def protected(authorization: str = Header()):  # ✅ Works with Pylance
    # def protected(password: str, required_password: str = "secret"):
    """return success with valid token

    Args:
        authorization (str): authorization token

    Returns:
        str: "success" if token is valid, otherwise returns "invalid token"
    """
    if authorization == "token12345":
        # if password == required_password:
        return "Success!"
    return "invalid token"


@router.get("/userid")
async def get_userid(user: Annotated[dict, Depends(get_firebase_user_from_token)]):
    """gets the firebase connected user"""
    return {"id": user["uid"]}
