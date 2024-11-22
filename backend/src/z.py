import asyncio
import websockets
import json
from src.logger import logger


clients = set()

async def start_websocket_server():
    logger.info("Z")
    async def handle_connection(websocket, path):
        # Подключение нового клиента
        logger.info("ZZZZZ")
        clients.add(websocket)
        try:
            async for message in websocket:
                # Получаем сообщение от клиента
                logger.info(f"Received message: {message}")

                # Рассылаем это сообщение всем остальным клиентам
                for client in clients:
                    if client != websocket:
                        await client.send(message)
        except websockets.exceptions.ConnectionClosed:
            logger.info("Connection closed")
        finally:
            # Убираем клиента из списка при закрытии соединения
            clients.remove(websocket)

    # Запуск WebSocket сервера на порту 5000
    server = await websockets.serve(handle_connection, "skin-cancer.ru", 5000)
    logger.info("WebSocket server started at ws://localhost:5000")
    await server.wait_closed()
    
