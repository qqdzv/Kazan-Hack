from fastapi_cache.backends.redis import RedisCacheBackend
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import websockets
from src.auth.router import router as router_user
from src.ai_bot.router import router as router_ai
from src.scan.router import router as router_scan
from src.doctor.router import router as router_doctor
from src.messages.router import router as router_messages
from src.private_api.router import router as router_shared
from tgbot.bot import dp
from src.myredis import redis_fastapi
import asyncio
import time

templates = Jinja2Templates(directory="src/templates")

# Ваши WebSocket обработчики
clients = set()

async def handle_connection(websocket, path):
    # Подключение нового клиента
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
        # Убираем клиента из списка при закрытии соединенияx
        clients.remove(websocket)

async def start_websocket_server():
    server = await websockets.serve(handle_connection, "skin-cancer.ru", 5000)
    print("WebSocket server started at ws://:5000")
    await server.wait_closed()

# Асинхронный контекст жизни FastAPI для запуска WebSocket сервера
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запуск WebSocket сервера в фоновом режиме]
    bot_task = asyncio.create_task(start_tgbot())
    RedisCacheBackend(redis_fastapi)
    websocket_task = asyncio.create_task(start_websocket_server())
    yield  # Возвращаем управление FastAPI
    
    # Завершаем задачи после выхода из lifespan
    websocket_task.cancel()
    bot_task.cancel()
    await websocket_task
    await bot_task
    
async def start_tgbot():
    await dp.start_polling()
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    time.sleep(2)
    bot_task = asyncio.create_task(start_tgbot())
    RedisCacheBackend(redis_fastapi)
    yield
    
    bot_task.cancel()
    await bot_task

app = FastAPI(
    title="Test",
    lifespan=lifespan,
    root_path="/api",
)
    
app.include_router(router_scan)
app.include_router(router_user)
app.include_router(router_doctor)
app.include_router(router_ai)
app.include_router(router_messages)
app.include_router(router_shared)

origins = [
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000",
    "http://localhost:8000",
    "https://d037-185-244-218-22.ngrok-free.app",
    "https://skin-cancer.ru"
]

app.add_middleware(
    CORSMiddleware,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*'],
    allow_origins=['*'],
)

