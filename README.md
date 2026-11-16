# Full-Stack AWS IoT Core Project (Docker + Terraform + Live Web Dashboard)

This project combines:
1. **Terraform (`terraform/`)**: Infrastructure as Code (IaC) to automatically provision your AWS IoT Thing, IoT Policy, and X.509 certificates.
2. **Dockerized Sensor Node (`device.py` + `Dockerfile`)**: Publishes live `temperature` and `humidity` telemetry over MQTT + TLS (Port 8883).
3. **Live Web Dashboard (`frontend/`)**: A Flask + Chart.js + Tailwind CSS web application that subscribes to AWS IoT Core in real time and plots live interactive graphs at `http://localhost:5000`.
4. **Docker Compose (`docker-compose.yml`)**: Launches both the IoT sensor publisher and the live web dashboard with a single command.
