from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.routers import users,library,security,user_recomendation


app = FastAPI()

app.include_router(users.router, prefix="/user", tags=["user"])
app.include_router(library.router, prefix="/library", tags=["library"])
app.include_router(user_recomendation.router, prefix="/recomendation", tags=["recomendation"])
app.include_router(security.router, prefix="/security", tags=["security"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(GZipMiddleware)