from fastapi import FastAPI
from app.routers import books

app= FastAPI(
    title="Book Inventory API",
    description="A CRUD API for managing book inventory with 3-layer architecture",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc UI
)

app.include_router(books.router)
@app.get("/", tags=["root"])
def read_root():
    return{
        "message": "Welcome to Book Inventory API v2.0 - CI/CD is Working! 🚀",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
   # uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
   #for azure
    uvicorn.run(app, host="0.0.0.0", port=8000)