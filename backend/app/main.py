from fastapi import FastAPI

app = FastAPI(title="Universal AI Documentation System Design Companion Backend")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Universal AI Documentation System Design Companion Backend"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

