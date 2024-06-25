from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.user import router as user_router
from app.config.database import lifespan

app: FastAPI = FastAPI(
    lifespan=lifespan,
    title="Full-Auth-App",
    servers=[{"url": "http://127.0.0.1:8002", "description": "Auth server"}]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000",],  # Or specify the domain of your Swagger UI
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "Auth with FastAPI"}
