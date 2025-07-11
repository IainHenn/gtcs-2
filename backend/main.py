from fastapi import FastAPI, Request
import httpx

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/submit")
async def read_data(request: Request):
    async with httpx.AsyncClient() as client:
        data = await request.json()
        print(f"data: {data}")
        data_dict = {}
        data_dict["data"] = data
        return data_dict