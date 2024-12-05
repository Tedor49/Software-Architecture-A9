import sys, os
from time import sleep
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

app = FastAPI()

connection = None
for i in range(10):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('host.docker.internal'))
        break
    except pika.exceptions.AMQPConnectionError:
        sleep(1)

if connection == None:
    print("Could not connect to rabbitmq", file=sys.stderr, flush=True)
    exit(-1)

print("Connected to RabbitMQ!", flush=True)

channel = connection.channel()

channel.queue_declare(queue='api->filter')

@app.post("/")
async def post_message(item: Message, response: Response) -> Status:
    try:
        channel.basic_publish(exchange='',
          routing_key='api->filter',
          body=dumps({"user": item.user, "msg": item.message}))
        
        return {"success": True}
    except Exception as e:
        response.status_code = 500
        return {"success": False}


if __name__ == '__main__':
    try:
        uvicorn.run("api:app", host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        connection.close()
        print('Stopped')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
