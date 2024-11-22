import asyncio
import websockets
import json
from src.logger import logger


clients = set()

async def start_websocket_server():
    logger.info("Z")
    async def handle_connection(websocket, path):
        logger.info(f"New connection: {path}")
        clients.add(websocket)
        try:
            async for message in websocket:
                logger.info(f"Received message: {message}")
                for client in clients:
                    if client != websocket:
                        try:
                            await client.send(message)
                        except Exception as e:
                            logger.error(f"Error sending message: {e}")
        except Exception as e:
            logger.error(f"Connection error: {e}")
        finally:
            clients.remove(websocket)
            logger.info("Client disconnected")


    # Запуск WebSocket сервера на порту 5000
    server = await websockets.serve(handle_connection, "0.0.0.0", 5000)
    logger.info("WebSocket server started at ws://0.0.0.0/ws:5000")
    await server.wait_closed()
    logger.info("WebSocket server closed at ws://0.0.0.0/ws:5000")
