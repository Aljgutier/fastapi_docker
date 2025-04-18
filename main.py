# main.py
"""
FastAPI Hello World, Getting Started application, main.py

"""

from fastapi import FastAPI
from app.router import router


# initialize app
app = FastAPI()

app.include_router(router)
