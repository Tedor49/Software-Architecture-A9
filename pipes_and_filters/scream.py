from multiprocessing import Event, Process
from queue import Empty

class Scream:
    def __init__(self, input_pipe, output_pipe):
        self.in_pipe = input_pipe
        self.out_pipe = output_pipe
        
        self.stopped = Event()
        self.proc = Process(target=self.run, daemon=True)
        self.proc.start()

    def run(self):
        while not self.stopped.is_set():
            try:
                item = self.in_pipe.get(timeout=0.2)
                item["msg"] = item["msg"].upper()
                self.out_pipe.put(item)
            except Empty:
                continue

    def graceful_exit(self):
        self.stopped.set()
        self.proc.join()

