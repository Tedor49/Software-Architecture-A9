import multiprocessing
from api import run_api
from filter import Filter
from scream import Scream
from publish import Publish

if __name__ == "__main__":
    manager = multiprocessing.Manager()

    log_pipe = manager.Queue()
    
    pipe1, pipe2, pipe3 = manager.Queue(), manager.Queue(), manager.Queue()
    
    filt = Filter(pipe1, pipe2)
    scream = Scream(pipe2, pipe3)
    publish = Publish(pipe3, log_pipe)

    run_api(pipe1)
    
    for i in [filt, scream, publish]:
        i.graceful_exit()

    
