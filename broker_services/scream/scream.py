import sys, os
from time import sleep
from pickle import dumps, loads
import pika

def callback(ch, method, properties, body):
    global stop_words
    
    print("Received message!", flush=True)
    
    msg = loads(body)

    msg["msg"] = msg["msg"].upper()

    channel.basic_publish(exchange='',
      routing_key='scream->publish',
      body=dumps(msg))
    print("Sent message!", flush=True)

if __name__ == '__main__':
    try:
        print("I EXIST!", flush=True)
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

        channel.queue_declare(queue='filter->scream')
        channel.queue_declare(queue='scream->publish')
        
        channel.basic_consume(queue='filter->scream',
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
