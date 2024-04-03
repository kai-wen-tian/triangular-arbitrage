
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from config.config import settings
import uvicorn
import logging
#from app.services.arbitrage.triangular import execute_tri
from bootstrap.scheduler import create_scheduler

app = FastAPI()

connected_clients = set()
"""
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            result = execute_tri()
            await websocket.send_text(result)
    except Exception as e:
        logging.error(f"WebSocket connection closed with exception: {e}")
    finally:
        connected_clients.remove(websocket)

"""

@app.get("/")
async def root():
    return "Welcome to FastAPI Skeleton"

async def send_message(message: str):
    for client in connected_clients:
        await client.send_text(message)


class CustomList(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def append(self, item):
        super().append(item)
        print(f"Item '{item}' appended to the list")

#global custom_list
#global custom_list
#custom_list = CustomList()



if __name__ == "__main__":
    scheduler=create_scheduler()
    scheduler.start()
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
    