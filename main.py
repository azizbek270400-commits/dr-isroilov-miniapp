from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

DB = "db.json"

def load():
    with open(DB) as f:
        return json.load(f)

def save(data):
    with open(DB, "w") as f:
        json.dump(data, f)

WORK_HOURS = ["08:00","09:00","10:00","11:00","13:00","14:00","15:00","16:00","17:00","18:00"]

@app.get("/times/{date}")
def get_times(date):
    db = load()
    busy = [a["time"] for a in db["appointments"] if a["date"] == date]
    return [t for t in WORK_HOURS if t not in busy]

@app.post("/book")
def book(data: dict):
    db = load()
    db["appointments"].append(data)
    save(db)
    return {"status": "ok"}

@app.get("/my/{uid}")
def my(uid: int):
    db = load()
    return [a for a in db["appointments"] if a["uid"] == uid]