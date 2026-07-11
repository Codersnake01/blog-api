from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="Blog API",
    description="API de blog profesional con roles, categorías, etiquetas y comentarios",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api/v1")