from fastapi import FastAPI, Header
from pydantic import BaseModel


# initialize app
app = FastAPI()


# get hello world
@app.get("/")
def read_root():
    """
    Get root
    """
    return {"Hello": "World"}


# get with Path Parameters
@app.get("/greet/{name}")
def greet(name: str):
    """Get Items

    Args:
        name (str): url path parameter

    Returns:
        json: key:"hello", value: "world"
    """
    return f"Hello {name}"


# get with Query Parameters
@app.get("/items/")
def read_parameters(category: str, brand: str):
    """read query paraemters, key=value pairs in the url string

    Args:
        category (str): category query parameter
        brand (str): brand query paraemter

    Returns:
        dict: keys category and brand
    """
    return {"category": category, "brand": brand}


##### Post with Pydantic Body/Data Model


class ItemPost(BaseModel):
    """Post Body/Data Model

    Args:
        BaseModel (BaeModel): Pydantic Base Model
    """

    name: str
    description: str = None
    price: float
    tax: float = None


@app.post("/items_post/")
def create_item(item: ItemPost):
    """Create item from post
    Args:
        item (ItemPost): item following the ItemPost model

    Returns:
        ItemPost: returns the item
    """
    return item


##### Get with Pydantic Return Model
class ItemGet(BaseModel):
    """Get Model

    Args:
        BaseModel (BaseModel): PyDantic Base Model
    """

    name: str
    description: str
    price: float


@app.get("/items_get/")
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


###### Authenticated Protected
@app.get("/protected")
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
