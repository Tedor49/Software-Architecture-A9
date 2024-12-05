import sys, os
from time import time_ns, sleep
import smtplib
from email.message import EmailMessage
from pickle import dumps, loads
import pika

SERVER_IP = 'mail.smtp2go.com'
SERVER_PORT = 465

SENDER_LOGIN = 'softarch_a9'
SENDER_PASSWORD = 'acmHxX0WWOqA5tfG'

mailing_list = ["f.smirnov@innopolis.university",
                "i.lishchenko@innopolis.university",
                "al.morozov@innopolis.university",
                "t.suleymanov@innopolis.university"]
                
#mailing_list = ["f.smirnov@innopolis.university"]

def callback(ch, method, properties, body):
    global stop_words, server
    
    print("Received message!", flush=True)

    data = loads(body)
        
    for mail in mailing_list:
        msg = EmailMessage()
        msg.set_content(f"From user: {data['user']}\n\nMessage: {data['msg']}")

        msg['From'] = "f.smirnov@innopolis.university"
        msg['To'] = mail

        server.send_message(msg)
    print("Sent emails!", flush=True)
    print("Time: ", time_ns(), flush=True)

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
            print("Could not connect to rabbitmq", file=sys.stderr)
            exit(-1)

        print("Connected to RabbitMQ!", flush=True)

        channel = connection.channel()

        channel.queue_declare(queue='scream->publish')
        
        channel.basic_consume(queue='scream->publish',
          auto_ack=True,
          on_message_callback=callback)

        server = smtplib.SMTP_SSL(SERVER_IP, SERVER_PORT)
        server.login(SENDER_LOGIN, SENDER_PASSWORD)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        server.quit()
        connection.close()
        print('Stopped')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
