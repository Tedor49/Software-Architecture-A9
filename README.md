# Demo

The video demo can be found at https://drive.google.com/file/d/1aCrVcQ_C3OPeG7UyFQ90vF3BQhffCS92/view

# Prerequisites

Make sure you have docker and python >= 3.7 with pip and run
```
pip install pika fastapi[all]
```
# Running the scripts

After running either of the versions, you can find the API at localhost:8000. There are also swagger docs available at localhost:8000/docs

## Broker topology version

To run the version with brokers and services navigate to the broker_services folder and run
```
docker compose up
```
And to benchmark it for speed, run 
```
python benchmark_services.py
```
A version of the output of the benchmark can be found at broker_services/benchmark_logs.txt

## Pipes and Filters version

To run the version with pipes and filters navigate to the pipes_and_filters folder and run
```
python launch.py
```
And to benchmark it for speed, run 
```
python benchmark_pipes.py
```
A version of the output of the benchmark can be found at pipes_and_filters/benchmark_logs.txt

# Performance comparison

When it comes to time, both implementations are very close, with pipes and filters consistenwith brokers consistently a bit slower. We believe that this is because of the pipeline nature of both architectures: the processors can work on separate stages, so only the time of the longest stage, the bottleneck, is of most importance. In both topologies, the longest part is waiting for the SMTP server to reply, and as we are using the same one for both topologies, the times remain similar. However, the small increase in time from using broker topology definetely comes from us hosting separate services, so the payload constantly needs to travel through the network, which is more time-consuming that the basic IPC methods used in pipes-and-filters.

As for the memory consumption, it is indisputable: broker services take up more memory both on the hard drive and the RAM. The hard drive discrepancy because we need to store the built images instead of just the source code, and for the RAM, the Docker engine takes up a lot of memory for running virtualization, so it also cannot compare to multiple processes running on the same OS.
