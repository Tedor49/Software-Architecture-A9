import sys, os
from time import sleep
from pickle import dumps, loads
import pika

stop_words = ["bird-watching", "ailurophobia", "mango"]

def callback(ch, method, properties, body):
    global stop_words
       
    print("Received message!", flush=True)
    
    msg = loads(body)

    if not any(word in msg["msg"] for word in stop_words):
        channel.basic_publish(exchange='',
          routing_key='filter->scream',
          body=body)
        print("Sent message!", flush=True)
    else:
        print("Blocked message!", flush=True)

if __name__ == '__main__':
    try:
        connection = None
        print("I EXIST!", flush=True)
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
        channel.queue_declare(queue='filter->scream')
        
        channel.basic_consume(queue='api->filter',
          auto_ack=True,
          on_message_callback=callback)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        connection.close()
        print('Stopped')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
