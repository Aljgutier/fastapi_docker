# main.py
"""
FastAPI Hello World, Getting Started application, main.py

"""

# Firevase
import firebase_admin
from firebase_admin import credentials

# Corrs
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import router

# importing config will also call load_dotenv to get GOOGLE_APPLICATION_CREDENTIALS
from app.config import get_settings

# initialize app and routes
app = FastAPI()
app.include_router(router)

settings = get_settings()
origins = [settings.frontend_url]

# Fireebase
cred = credentials.Certificate(settings.google_application_credentials)

firebase_admin.initialize_app(cred)
# Debug ... Google FIrebase Check
print("Current App Name:", firebase_admin.get_app().project_id)

# Corrs
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
