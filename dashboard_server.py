"""
Web Dashboard Server for NeuroOps Duo.
Hosts the visual real-time execution dashboard for hackathon judges and video demonstrations.
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

app = FastAPI(title="NeuroOps Duo Visual Dashboard")

DASHBOARD_PATH = os.path.join(os.path.dirname(__file__), "dashboard", "index.html")

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    with open(DASHBOARD_PATH, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    print("==================================================================")
    print(" Starting NeuroOps Duo Visual Dashboard at: http://localhost:8000")
    print(" Use this in your browser to record the winning hackathon video!")
    print("==================================================================")
    uvicorn.run(app, host="127.0.0.1", port=8000)
