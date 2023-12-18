import io
import base64
import uvicorn
import numpy as np
from PIL import Image
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from predict_gesture import predict as gest_predict
from predict_hand_coord import predict as coord_predict
from check_direction import get_direction


app = FastAPI(title='server')


# настройка CORS для разрешения запросов с определенных источников
origins = [
    "http://localhost:3000"  # для тестирования
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", 'DELETE', 'PUT', 'PATCH'],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)


manager = ConnectionManager()


@app.websocket("/ws")
async def get_prediction(websocket: WebSocket):
    client_ip = websocket.client.host

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_bytes()

            # приводим изображение из байтов в массив numpy
            image_bytes = base64.b64decode(data)
            image = Image.open(io.BytesIO(image_bytes))
            image_np = np.array(image)

            # предиктим жест
            gest_prediction = gest_predict(image_np)

            # предиктим координаты руки
            coord_prediction = coord_predict(image_np)

            # определяем было ли движение влево или вправо
            if coord_prediction:
                m_direction = get_direction(client_ip, coord_prediction)

                if m_direction:
                    await websocket.send_text(m_direction)


            await websocket.send_text(gest_prediction)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


