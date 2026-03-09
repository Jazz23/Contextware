from fastapi import FastAPI
from typing import List, Dict

app = FastAPI()

# Placeholder for storage
tasks_metadata = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def list_tasks():
    return tasks_metadata

@app.get("/stats")
def get_stats():
    """
    TODO: Aggregate stats from storage and return them.
    Should include success rate, total tasks, and average latency.
    """
    return {"error": "Not implemented"}
