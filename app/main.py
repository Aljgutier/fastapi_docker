# main.py
"""
FastAPI Hello World, Getting Started application, main.py

"""

# Firevase
import firebase_admin

# Corrs
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from app.router import router

# importing config will also call load_dotenv to get GOOGLE_APPLICATION_CREDENTIALS
from app.config import get_settings

# initialize app and routes
app = FastAPI()
app.include_router(router)

settings = get_settings()
origins = [settings.frontend_url]

# Fireebase
firebase_admin.initialize_app()
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
