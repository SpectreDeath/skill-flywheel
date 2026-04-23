"""Evolution routes with WebSocket support."""

import asyncio
import json
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, WebSocket, WebSocketDisconnect
from flywheel.evolution import tasks

router = APIRouter(prefix="/evolution", tags=["Evolution"])


class ConnectionManager:
    """Manage WebSocket connections for evolution progress."""

    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, job_id: str):
        await websocket.accept()
        self.active_connections[job_id] = websocket

    def disconnect(self, job_id: str):
        self.active_connections.pop(job_id, None)

    async def send_progress(self, job_id: str, data: dict):
        if job_id in self.active_connections:
            await self.active_connections[job_id].send_json(data)


manager = ConnectionManager()


@router.websocket("/ws/{job_id}")
async def evolution_progress(websocket: WebSocket, job_id: str):
    """WebSocket endpoint for real-time evolution progress."""
    await manager.connect(websocket, job_id)
    try:
        while True:
            status = tasks.get_job_status(job_id)
            if status:
                await websocket.send_json(status.to_dict())
                if status.status in ["completed", "failed"]:
                    break
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(job_id)


@router.post("/start")
async def start_evolution(
    initial_genome: dict,
    max_generations: int = Query(10, ge=1, le=100),
):
    """Start a new evolution job."""
    try:
        job_id = tasks.start_evolution_job(
            initial_genome_data=initial_genome,
            max_generations=max_generations,
        )
        return {"job_id": job_id, "status": "started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{job_id}")
async def get_evolution_status(job_id: str):
    """Get evolution job status."""
    status = tasks.get_job_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return status.to_dict()
