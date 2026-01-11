
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json, datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

DB = "db.json"
ADMIN_ID = 5096290302

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
    data["status"] = "pending"
    db["appointments"].append(data)
    save(db)
    return {"status": "ok"}

@app.get("/my/{uid}")
def my(uid: int):
    db = load()
    return [a for a in db["appointments"] if a["uid"] == uid]

@app.get("/admin/{date}/{uid}")
def admin(date: str, uid: int):
    if uid != ADMIN_ID:
        return {"error":"forbidden"}
    db = load()
    return [a for a in db["appointments"] if a["date"] == date]

@app.post("/confirm")
def confirm(data: dict):
    db = load()
    for a in db["appointments"]:
        if a["uid"]==data["uid"] and a["date"]==data["date"] and a["time"]==data["time"]:
            a["status"]="confirmed"
    save(db)
    return {"ok":True}

@app.post("/cancel")
def cancel(data: dict):
    db = load()
    db["appointments"] = [a for a in db["appointments"] if not (a["uid"]==data["uid"] and a["date"]==data["date"] and a["time"]==data["time"])]
    save(db)
    return {"ok":True}
