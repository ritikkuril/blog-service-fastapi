from fastapi import FastAPI
from app.database import engine, Base
from app.routers import blogs


app = FastAPI(title="Blog Service API")

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(blogs.router)

@app.get("/")
def root():
    return {"message": "Blog API is running"}
