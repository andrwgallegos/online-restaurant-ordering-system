from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import model_loader
from .routers import index as index_route

app = FastAPI(title="Online Restaurant Ordering System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
index_route.load_routes(app)