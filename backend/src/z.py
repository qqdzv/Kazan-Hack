import asyncio
import websockets
import json

clients = set()

async def start_websocket_server():
    print("Z")
    async def handle_connection(websocket, path):
        # Подключение нового клиента
        print("ZZZZZ")
        clients.add(websocket)
        try:
            async for message in websocket:
                # Получаем сообщение от клиента
                print(f"Received message: {message}")

                # Рассылаем это сообщение всем остальным клиентам
                for client in clients:
                    if client != websocket:
                        await client.send(message)
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
        finally:
            # Убираем клиента из списка при закрытии соединения
            clients.remove(websocket)

    # Запуск WebSocket сервера на порту 5000
    server = await websockets.serve(handle_connection, "skin-cancer.ru", 5000)
    print("WebSocket server started at ws://localhost:5000")
    await server.wait_closed()
    
