from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
import os
from fastapi.middleware.cors import CORSMiddleware
import attendance

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/submit")
async def submit(data: dict):
    name, status = data.get("name"), data.get("status")
    if not name or not status:
        raise HTTPException(status_code=400, detail="Key and value required")

    attendance.add(name, status)
    return {"message": "Key-value pair stored successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
