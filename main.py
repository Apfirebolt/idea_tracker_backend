from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from typing import List
import uvicorn
from logging_config import setup_logging
from contextlib import asynccontextmanager
import logging

# RabbitMQ imports
from backend.core.rabbitmq import connect_rabbitmq, get_rabbitmq_channel # Import the new functions

from backend.middleware import TimingMiddleware
from fastapi_pagination import add_pagination

from backend.auth import router as auth_router
from backend.ideas import router as ideas_router
from backend.users import router as users_router
from backend.tags import router as tags_router
from backend.scripts import router as scripts_router

# 1. Call setup_logging() once at the application's entry point
setup_logging()

# 2. Get the *configured* logger instance by its name
logger = logging.getLogger("idea_app")

_rabbitmq_connection = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager for managing application startup and shutdown events.
    """
    global _rabbitmq_connection # Declare intent to modify the global variable

    logger.info("Application starting up...")
    try:
        # Connect to RabbitMQ
        _rabbitmq_connection = await connect_rabbitmq()
        # print connected if successful
        if _rabbitmq_connection and not _rabbitmq_connection.is_closed:
            logger.info("RabbitMQ connection established successfully.")
        else:
            logger.warning("RabbitMQ connection is closed or not established.")
        logger.info("RabbitMQ connection established during startup.")

        yield # Yield control to the application (FastAPI will start serving requests)

    except Exception as e:
        logger.critical(f"Failed during startup events: {e}", exc_info=True)
        raise

    finally:
        logger.info("Application shutting down...")
        # Close RabbitMQ connection
        if _rabbitmq_connection and not _rabbitmq_connection.is_closed:
            await _rabbitmq_connection.close()
            logger.info("RabbitMQ connection closed during shutdown.")
        else:
            logger.warning("RabbitMQ connection was not open or already closed during shutdown.")


app = FastAPI(title="Fast API Ticket Master App",
    description="A FastAPI application for managing ideas, users, and tags with WebSocket support.",
    docs_url="/docs",
    lifespan=lifespan,
    version="0.0.1")

origins = ["http://localhost:8080", "http://localhost:3000",]

# Add pagination
add_pagination(app)

# Add the timing middleware
app.add_middleware(TimingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(ideas_router.router)
app.include_router(users_router.router)
app.include_router(tags_router.router)
app.include_router(scripts_router.router)

# ConnectionManager class to handle active WebSocket connections
class ConnectionManager:
    def __init__(self):
        # List to store active WebSocket connections
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
        Accepts a new WebSocket connection and adds it to the active_connections list.
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"New connection established: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        """
        Removes a disconnected WebSocket from the active_connections list.
        """
        self.active_connections.remove(websocket)
        print(f"Connection disconnected: {websocket.client}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """
        Sends a message to a specific WebSocket client.
        """
        await websocket.send_text(message)
        print(f"Sent personal message to {websocket.client}: {message}")

    async def broadcast(self, message: str):
        """
        Sends a message to all active WebSocket clients.
        """
        print(f"Broadcasting message: {message}")
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except RuntimeError as e:
                # Handle cases where connection might have closed unexpectedly
                print(f"Error sending to {connection.client}: {e}. Removing connection.")
                self.disconnect(connection)

# Create an instance of the ConnectionManager
manager = ConnectionManager()

# WebSocket endpoint for chat
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """
    Handles WebSocket connections for chat.
    Each client connects with a unique client_id.
    """
    await manager.connect(websocket)
    await manager.broadcast(f"Client #{client_id} joined the chat")
    try:
        while True:
            # Receive text data from the WebSocket
            data = await websocket.receive_text()
            # Broadcast the received message to all connected clients
            await manager.broadcast(f"Client #{client_id}: {data}")
    except WebSocketDisconnect:
        # Handle client disconnection
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred with client {client_id}: {e}")
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} had an error and left the chat.")


@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the FastAPI Idea Tracker App!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)