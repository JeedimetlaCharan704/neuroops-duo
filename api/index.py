"""
Vercel Serverless Entrypoint for NeuroOps Duo.
Serves the FastAPI application and the interactive DevSecOps dashboard.
"""
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from fastapi.responses import HTMLResponse
from target_service.app import app

DASHBOARD_FILE = os.path.join(ROOT_DIR, "dashboard", "index.html")

@app.get("/", response_class=HTMLResponse)
async def serve_root_dashboard():
    if os.path.exists(DASHBOARD_FILE):
        with open(DASHBOARD_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>NeuroOps Duo Dashboard Active</h1>"

# Vercel entrypoint
application = app
