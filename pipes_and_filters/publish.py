import sys

from multiprocessing import Event, Process
from queue import Empty
import smtplib
from email.message import EmailMessage
from time import time_ns

SERVER_IP = 'mail.smtp2go.com'
SERVER_PORT = 465

SENDER_LOGIN = 'softarch_a9'
SENDER_PASSWORD = 'acmHxX0WWOqA5tfG'

mailing_list = ["f.smirnov@innopolis.university",
                "i.lishchenko@innopolis.university",
                "al.morozov@innopolis.university",
                "t.suleymanov@innopolis.university"]
                
#mailing_list = ["f.smirnov@innopolis.university"]

class Publish:
    def __init__(self, input_pipe, log_pipe):
        self.pipe = input_pipe
        self.log_pipe = input_pipe
        
        self.stopped = Event()
        self.proc = Process(target=self.run, daemon=True)
        self.proc.start()

    def run(self):
        self.server = smtplib.SMTP_SSL(SERVER_IP, SERVER_PORT)
        self.server.login(SENDER_LOGIN, SENDER_PASSWORD)
        
        logs = open("publish_logs.txt", "wb", buffering=0)
        
        while not self.stopped.is_set():
            try:
                item = self.pipe.get(timeout=0.2)
                
                logs.write(b"Recieved message!\n")
                
                for mail in mailing_list:
                    msg = EmailMessage()
                    msg.set_content(f"From user: {item['user']}\n\nMessage: {item['msg']}")

                    msg['From'] = "f.smirnov@innopolis.university"
                    msg['To'] = mail

                    self.server.send_message(msg)
                logs.write(b"Sent messages!\n")
                logs.write(f"Time: {time_ns()}\n".encode())
            except Empty:
                continue

    def graceful_exit(self):
        self.stopped.set()
        self.proc.join()

