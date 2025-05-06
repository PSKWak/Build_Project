##Synthetic Monitoring Platform
This project was developed as part of the Build Fellowship offered by Open Avenue, under the mentorship of Sonu Gupta. The primary aim is to monitor the health, availability, and performance of websites (or web servers) in real-time, ensuring they are accessible and responsive to users. The dashboard, created using Grafana, proactively tracks key metrics such as response time, status code, and availability by sending periodic HTTP requests, with metrics exposed in Prometheus format.
Features

Monitors websites for uptime, response time, and HTTP status codes.
Exposes metrics via a Prometheus-compatible endpoint (http://localhost:8989/metrics).
Real-time Grafana dashboard for visualizing website health and performance.
Configurable list of websites to monitor (e.g., https://www.google.com, or an EC2 web server like http://184.72.155.124).
Lightweight and extensible for additional metrics or alerting.

#Prerequisites

Python 3.6+: With requests and prometheus_client libraries.
Prometheus: Version 3.4.0-rc.0 or later (Windows binary recommended).
Grafana: For dashboard visualization.
Windows: Instructions are tailored for Windows, but adaptable for Linux/macOS.
AWS EC2 (Optional): If monitoring an EC2 instance (e.g., 184.72.155.124), ensure it hosts a web server with HTTP (port 80) or HTTPS (port 443) allowed in the security group.

#Installation
1. Clone the Repository
git clone https://github.com/your-username/website-monitoring.git
cd website-monitoring

2. Install Python Dependencies
Install the required Python libraries:
pip install requests prometheus_client

3. Configure the Monitoring Script
The monitoring script (website_monitor.py) sends HTTP requests to a list of websites and exposes metrics.

Open website_monitor.py in a text editor.
Update the CONFIG dictionary to include the websites you want to monitor:CONFIG = {
    "websites": [
        "https://www.google.com",
        "https://www.example.com",
        # Add your EC2 instance: "http://184.72.155.124"
    ],
    "interval": 10,  # Seconds between checks
    "timeout": 5    # HTTP request timeout
}


EC2 Note: If monitoring 184.72.155.124, ensure the EC2 instance has a web server (e.g., Apache, Nginx) and allows HTTP traffic (security group inbound rule: HTTP, port 80, source 0.0.0.0/0).

4. Run the Monitoring Script
Start the Python script to begin monitoring websites:
cd C:\Users\HP\monitoring
python website_monitor.py


The script exposes metrics at http://localhost:8989/metrics.
Expected output:Prometheus metrics server started on port 8989...
Checking https://www.google.com...
Status Code: 200, Response Time: 0.123s



5. Configure and Run Prometheus
Prometheus scrapes metrics from the Python script.

Verify prometheus.yaml:
Location: C:\Users\HP\prometheus-3.4.0-rc.0.windows-amd64\prometheus-3.4.0-rc.0.windows-amd64
Ensure it contains:global:
  scrape_interval: 15s
  evaluation_interval: 15s
scrape_configs:
  - job_name: 'website-monitoring'
    static_configs:
      - targets: ['localhost:8989']




Run Prometheus:cd C:\Users\HP\prometheus-3.4.0-rc.0.windows-amd64\prometheus-3.4.0-rc.0.windows-amd64
prometheus.exe --config.file=prometheus.yaml


Access the Prometheus UI at http://localhost:9090.
Verify the website-monitoring target is “UP” under “Status” > “Targets”.

6. Configure and Run Grafana
Grafana visualizes the metrics in a real-time dashboard.

Start Grafana:
Grafana typically runs as a service. If not, start it manually:cd C:\Program Files\GrafanaLabs\grafana\bin
grafana-server.exe


Access: http://localhost:3000 (default login: admin/admin).


Add Prometheus Data Source:
Go to “Configuration” > “Data Sources” > “Add data source”.
Select “Prometheus”.
Set URL: http://localhost:9090.
Click “Save & Test”.


Create a Dashboard:
Go to “Create” > “Dashboard” > “Add new panel”.
Add panels for:
Response Time:
Query: website_response_time_seconds
Visualization: Time series graph
Legend: {{url}}


Availability:
Query: website_is_up
Visualization: Gauge (thresholds: 0 = red, 1 = green)
Legend: {{url}}


Status Code:
Query: website_status_code
Visualization: Stat panel
Legend: {{url}}




Save the dashboard (e.g., “Website Health Dashboard”).



Usage

Run website_monitor.py to start monitoring websites.
Launch Prometheus to scrape metrics.
Access the Grafana dashboard at http://localhost:3000 to view real-time website health and performance.
Monitor metrics like response time, availability, and status codes for each website.

Ports

8989: Python script’s metrics endpoint (http://localhost:8989/metrics).
9090: Prometheus UI (http://localhost:9090).
3000: Grafana dashboard (http://localhost:3000).

Troubleshooting

Python Script Errors:
Ensure websites are accessible and EC2 instances allow HTTP.
Test: curl http://184.72.155.124.
Verify dependencies: pip show requests prometheus_client.


Prometheus Fails:
Check prometheus.yaml for correct syntax and file presence.
Ensure localhost:8989 is accessible: curl http://localhost:8989/metrics.


Grafana No Data:
Verify Prometheus is running and the data source URL is correct.
Confirm metric names (e.g., website_response_time_seconds) match.


Port Conflicts:
Check ports: netstat -aon | findstr :8989.
Change ports in website_monitor.py or prometheus.yaml if needed.


EC2 Issues:
Ensure the EC2 security group allows HTTP (port 80) or HTTPS (port 443).
Test: curl http://184.72.155.124.



Project Context
This project was built as part of the Build Fellowship by Open Avenue, mentored by Sonu Gupta. It aims to provide a robust solution for monitoring website health, with potential applications for production environments, including AWS EC2-hosted web servers.



