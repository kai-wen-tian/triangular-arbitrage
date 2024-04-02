
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from config.config import settings
import uvicorn
import logging

app = FastAPI()

connected_clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            from app.services.arbitrage.triangular import execute_tri
            result = execute_tri()
            await websocket.send_text(result)
    except Exception as e:
        logging.error(f"WebSocket connection closed with exception: {e}")
    finally:
        connected_clients.remove(websocket)

@app.get("/")
async def root():
    return "Welcome to FastAPI Skeleton"
async def send_message(message: str):
    for client in connected_clients:
        await client.send_text(message)
if __name__ == "__main__":
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
