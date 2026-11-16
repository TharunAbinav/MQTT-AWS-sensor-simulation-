# IoT Communication Over Wireless Networks Using AWS IoT Core

A production-grade, containerized full-stack IoT project demonstrating secure cloud integration with simulated multi-sensor telemetry, Infrastructure-as-Code (Terraform), MQTT over TLS, and a real-time web visualization dashboard.

---

## 🏗️ System Architecture

```text
       +-----------------------+
       |   Docker Container    |
       |  (Simulated Sensor)   |
       +-----------+-----------+
                   |
                   | MQTT over TLS v1.2 (Port 8883)
                   | X.509 Certificates
                   v
       +-----------------------+
       |     AWS IoT Core      | (Provisioned via Terraform)
       +-----------------------+
            |             |
            |             | MQTT Subscription
            v             v
    +---------------+   +------------------------------------+
    | AWS MQTT Test |   | Flask Web Dashboard (Port 5000)    |
    |    Client     |   | - Chart.js Live Graphs             |
    +---------------+   | - Tailwind CSS Dark UI             |
                        +------------------------------------+
```

---

## 🚀 Key Features

- **Secure Cloud Integration:** Implements mutual TLS (mTLS) authentication using X.509 certificates and Amazon Trust Services root CA over port 8883.
- **Dual-Sensor Telemetry Emulation:** Containerized Python publisher generating concurrent temperature ($\text{°C}$) and humidity ($\%$) payloads with UTC timestamps.
- **Infrastructure as Code (IaC):** Automated provisioning of AWS IoT Things, security policies, certificates, and endpoints using Terraform.
- **Real-Time Web Dashboard:** Flask backend subscriber paired with a modern Tailwind CSS and Chart.js frontend rendering live time-series charts.
- **Docker Compose Orchestration:** Single-command deployment of both the sensor node and the web dashboard application.

---

## 📂 Project Structure

```text
iot-fullstack-project/
├── certs/                        # X.509 security certificates & Root CA
├── terraform/                    # Infrastructure as Code (AWS IoT Core)
│   ├── main.tf                   # Provisions Thing, Policy, and Certs
│   ├── variables.tf              # Configurable region & resource names
│   └── outputs.tf                # Outputs AWS IoT Data-ATS endpoint
├── frontend/                     # Real-Time Web Dashboard
│   ├── app.py                    # Flask server + MQTT subscriber thread
│   ├── Dockerfile                # Container definition for web app
│   ├── requirements.txt          # Python dependencies (Flask, paho-mqtt)
│   └── templates/
│       └── index.html            # Dark-mode dashboard UI with Chart.js
├── device.py                     # Simulated multi-sensor publisher script
├── Dockerfile                    # Container definition for sensor publisher
├── docker-compose.yml            # Multi-container orchestration
└── .env.example                  # Environment variables template
```

---

## ⚙️ Prerequisites

1. **Docker Desktop** installed and running on your machine.
2. **Terraform** (Optional, if provisioning infrastructure automatically).
3. An active **AWS Account** with permissions for AWS IoT Core.

---

## 🛠️ Quick Start Guide

### Step 1: Obtain AWS IoT Certificates & Endpoint
You can either provision infrastructure using Terraform or place your existing AWS IoT Core certificates inside the `certs/` folder:
- `AmazonRootCA1.pem`
- `certificate.pem.crt`
- `private.pem.key`

### Step 2: Configure Environment Variables
Copy or create a `.env` file in the root directory with your AWS IoT endpoint:
```env
AWS_IOT_ENDPOINT=your-endpoint-ats.iot.us-east-1.amazonaws.com
```

### Step 3: Launch with Docker Compose
Open your terminal in the project root folder and run:
```bash
docker compose up --build
```

### Step 4: Access the Live Dashboard
Open your web browser and navigate to:
**`http://localhost:5000`**

---

## 🛑 Teardown

To stop all running containers gracefully, press `Ctrl + C` in your terminal or run:
```bash
docker compose down
```