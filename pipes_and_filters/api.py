import sys, os
from pickle import dumps, loads
import pika
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import uvicorn

class Message(BaseModel):
    user: str
    message: str

class Status(BaseModel):
    success: bool

def run_api(output_queue):
    run_api.app = FastAPI()

    @run_api.app.post("/")
    async def post_message(item: Message, response: Response) -> Status:
        try:
            output_queue.put({"user": item.user, "msg": item.message})
            return {"success": True}
        except Exception as e:
            response.status_code = 500
            return {"success": False}

    try:
        uvicorn.run("api:run_api.app", host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        pass
