# import asyncio
# import websockets
# import json

# # Хранение подключений клиентов
# clients = set()

# async def handle_connection(websocket, path):
#     # Подключение нового клиента
#     clients.add(websocket)
#     try:
#         async for message in websocket:
#             # Получаем сообщение от клиента
#             print(f"Received message: {message}")

#             # Рассылаем это сообщение всем остальным клиентам
#             for client in clients:
#                 if client != websocket:
#                     await client.send(message)
#     except websockets.exceptions.ConnectionClosed:
#         print("Connection closed")
#     finally:
#         # Убираем клиента из списка при закрытии соединения
#         clients.remove(websocket)

# # Запуск WebSocket сервера на порту 5000
# async def start_server():
#     server = await websockets.serve(handle_connection, "localhost", 5000)
#     print("WebSocket server started at ws://sk:5000")
#     await server.wait_closed()

# # Запуск сервера
# asyncio.run(start_server())
