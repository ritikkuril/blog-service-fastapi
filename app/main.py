from fastapi import FastAPI
from app.database import engine, Base
from app.routers import blogs, auth



app = FastAPI(title="Blog Service API")

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(blogs.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Blog API is running"}
