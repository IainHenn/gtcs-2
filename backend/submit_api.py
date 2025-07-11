from fastapi import FastAPI, Request
from pydantic import BaseModel
from tasks import reserve_campsite
from multiprocessing import Process

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReservationRequest(BaseModel):
    name: str
    password: str
    campID: str
    numSites: int
    startDate: str
    endDate: str

@app.post("/submit/")
async def submit_reservation(req: ReservationRequest):
    processes = []
    for i in range(5):
        p = Process(
            target=reserve_campsite,
            args=(req.name, req.password, req.campID, req.numSites, req.startDate, req.endDate)
        )
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
        
    return {"status": "submitted"}
