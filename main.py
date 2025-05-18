from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
import time
import uvicorn

from backend.auth import router as auth_router
from backend.ideas import router as ideas_router
from backend.users import router as users_router
from backend.tags import router as tags_router

app = FastAPI(title="Fast API Ticket Master App",
    docs_url="/docs",
    version="0.0.1")

origins = ["http://localhost:3000",]

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


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Idea Tracker App!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
 
