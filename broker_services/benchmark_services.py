from time import time_ns, sleep
from requests import post, get
import subprocess

API_IP = "http://localhost:8000/"

if __name__ == "__main__":

    all_logs = open("system-logs.txt", "wb")

    subprocess.run(["docker", "compose", "build"])
    system = subprocess.Popen(["docker", "compose", "up"], stdout=all_logs, stderr=all_logs)

    while True:
        try:
            print("Trying to connect to api...")
            succ = get(API_IP)
            break
        except Exception as e:
            sleep(1)
            #print(e)
            continue
    print("Connected!")

    ITER = 50

    start_times = []

    for i in range(ITER):
        if i % 10 == 0:
            print(f"Pushing message {i}")
        start_times.append(time_ns())
        response = post(API_IP, json={
          "user": f"test{i}",
          "message": "i love load testing"
        })
        if i % 10 == 0:
            print(response.content)
    
    print("FINISHED PUSHING ALL MESSAGES, WAITING FOR THE BROKER TO FINISH")
    
    print("0 %")
    
    logs = []
    while len(logs) != ITER:
        try:
            new_logs = subprocess.check_output(['docker', 'compose', 'logs', 'publish'])
            new_logs = list(map(lambda x: int(x.split()[-1]), filter(lambda x: "Time" in x, new_logs.decode().split("\n"))))
            if len(new_logs) > len(logs):
                print(len(new_logs) / ITER * 100, "%")
                logs = new_logs
        except subprocess.CalledProcessError:
            pass

    subprocess.run(["docker", "compose", "down"])
    all_logs.close()
    
    durations = []

    for j in range(ITER):
        durations.append(logs[j] - start_times[j])

    print(f"Average time using services: {sum(durations) / len(durations) / 1000000000}s")

