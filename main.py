from fastapi import FastAPI, WebSocket, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocketDisconnect
from typing import List, Annotated, Optional
from SocketManager import SocketManager
from routes import ManageChatroomsRoute

 

app = FastAPI()
# Mount static files
app.mount("/static", StaticFiles(directory="public"), name="static")
app.include_router(ManageChatroomsRoute.router,prefix="/chatrooms",tags=["chatrooms"])
manager = SocketManager()


@app.get("/")
async def get_index():
    """Serve the chat HTML page"""
    with open("public/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)



@app.websocket("/ws/{join_id}")
async def websocket_endpoint(websocket: WebSocket, join_id: str):
    await manager.connect(websocket, join_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast only to users in this specific room
            await manager.broadcast(join_id, data)
    except WebSocketDisconnect:
        await manager.disconnect(join_id, websocket)
