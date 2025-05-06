import yaml
import json
import time
import pingparsing
from prometheus_client import start_http_server, Gauge

# Define Prometheus metrics with a label for the server
rtt_min = Gauge("rtt_minimum", "Minimum RTT value in milliseconds", ["server"])
rtt_max = Gauge("rtt_maximum", "Maximum RTT value in milliseconds", ["server"])
rtt_avg = Gauge("rtt_average", "Average RTT value in milliseconds", ["server"])
packet_transmit = Gauge("packet_transmit", "Number of packets transmitted", ["server"])
packet_receive = Gauge("packet_receive", "Number of packets received", ["server"])
packet_loss_count = Gauge("packet_loss_count", "Number of packets lost", ["server"])
packet_loss_rate = Gauge("packet_loss_rate", "Packet loss percentage", ["server"])


try:
    with open("servers.yml", "r") as f:
        config = yaml.safe_load(f)
        servers = config.get("servers", [])
        interval = config.get("interval", 10)
    print("Configuration loaded successfully:")
    print(json.dumps(config, indent=4))
except FileNotFoundError:
    print("Error: sample.yml not found. Using default configuration.")
    servers = ["184.72.155.124"]  # Fallback to EC2 IP
    interval = 10
except yaml.YAMLError as e:
    print(f"Error: Invalid YAML format in sample.yml: {e}")
    servers = ["184.72.155.124"]
    interval = 10

# Initialize ping objects
ping_parser = pingparsing.PingParsing()
transmitter = pingparsing.PingTransmitter()
transmitter.count = 4

# Start Prometheus HTTP server
start_http_server(8989)
print("Prometheus metrics server started on port 8989...")


while True:
    for server in servers:
        print(f"\nPinging {server} {transmitter.count} times...")
        try:

            transmitter.destination = server
            result = transmitter.ping()
            parsed = ping_parser.parse(result).as_dict()


            print("Raw ping output:", result)
            print("Parsed metrics:")
            print(json.dumps(parsed, indent=4))


            rtt_min_val = parsed.get('rtt_min')
            rtt_max_val = parsed.get('rtt_max')
            rtt_avg_val = parsed.get('rtt_avg')


            rtt_min.labels(server=server).set(float(rtt_min_val) if rtt_min_val is not None else 0.0)
            rtt_max.labels(server=server).set(float(rtt_max_val) if rtt_max_val is not None else 0.0)
            rtt_avg.labels(server=server).set(float(rtt_avg_val) if rtt_avg_val is not None else 0.0)
            packet_transmit.labels(server=server).set(float(parsed.get('packet_transmit', 0)))
            packet_receive.labels(server=server).set(float(parsed.get('packet_receive', 0)))
            packet_loss_count.labels(server=server).set(float(parsed.get('packet_loss_count', 0)))
            packet_loss_rate.labels(server=server).set(float(parsed.get('packet_loss_rate', 0.0)))

        except Exception as e:
            print(f"Error pinging {server}: {e}")
            # Set metrics to indicate failure
            rtt_min.labels(server=server).set(0.0)
            rtt_max.labels(server=server).set(0.0)
            rtt_avg.labels(server=server).set(0.0)
            packet_transmit.labels(server=server).set(0.0)
            packet_receive.labels(server=server).set(0.0)
            packet_loss_count.labels(server=server).set(0.0)
            packet_loss_rate.labels(server=server).set(100.0)

        print(f"Waiting {interval} seconds before next ping...\n")
        time.sleep(interval)
