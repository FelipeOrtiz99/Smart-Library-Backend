from fastapi import FastAPI
from routers import users,library,security,user_recomendation

app = FastAPI()

app.include_router(users.router, prefix="/user", tags=["user"])
app.include_router(library.router, prefix="/library", tags=["library"])
app.include_router(user_recomendation.router, prefix="/recomendation", tags=["recomendation"])
app.include_router(security.router, prefix="/security", tags=["security"])
