from fastapi import FastAPI
from api import router
import uvicorn
app = FastAPI()
app.include_router(router)
@app.get("/")
async def root():
    return {"status": "running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)