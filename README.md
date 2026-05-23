# ⚡ Click Fast Analytics

A high-performance **OLAP (Online Analytical Processing)** dashboard engine that pairs **ClickHouse**'s columnar storage power with a highly performant and type-safe **FastAPI** service backend.

---

## 🚀 Key Features

* **⚡ Lightning-Fast Analytical Queries**: Streamlined execution directly against ClickHouse.
* **📦 Analytical Cube Configurations**: Pre-defined dimensional schemas mapping columns to dimensions (axises) and metrics (measures) to enable dynamic query generation.
* **🛡️ Type Safety & Validations**: Native Pydantic integration ensuring that client payloads are sanitized, validated, and documented automatically.
* **🐳 Complete Docker Orchestration**: Seamless multi-container workspace allowing one-command deployment.

---

## 📂 Project Organization

```text
├── clickhouse/             # ClickHouse DB configuration, backups & logs
│   ├── backups/            # Database storage files/backups
│   ├── config/             # ClickHouse server configuration XMLs
│   ├── user_scripts/       # User defined functions or automation scripts
│   └── test_nyc_taxi.sql   # SQL schema for the NYC Taxi benchmark dataset
├── fastapi/                # FastAPI application microservice
│   ├── app/                # Main application code
│   │   ├── clickhouse.py   # ClickHouse connector & query dispatcher
│   │   ├── main.py         # Main router, lifespan, and route definitions
│   │   └── scheme.py       # Pydantic schemas (e.g., ClickHouseModel)
│   ├── cube/               # Pre-configured analytical cube JSON specs
│   │   └── nyc_taxi.json   # NYC Taxi analytics cube schema definition
│   ├── req.txt             # Python requirements
│   ├── Dockerfile          # Multi-stage python base image
│   └── API_DOCUMENTATION.md# 📖 Standalone API Manual (New!)
└── docker-compose.yml      # Orchestration definition for local services
```

---

## 🛠️ Getting Started

### 1. Build and Run the Stack
To orchestrate and boot both ClickHouse and the FastAPI server, simply run:

```bash
docker compose up --build
```

### 2. Verify Database Seed
The ClickHouse container is configured to automatically download and initialize the NYC Taxi trips benchmark dataset. You can manually execute queries or verify the record count using `test_nyc_taxi.sql` or the `/clickhouse` endpoint.

---

## 📖 API Documentation & Reference

The FastAPI service generates interactive documentation automatically on startup:

* **Swagger UI (Interactive Playground)**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc (Reference Layout)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

For a complete guide including request flow diagram, curl command snippets, validation models, and detailed response schemas, read the dedicated API guide:

👉 **[API Reference Manual](fastapi/API_DOCUMENTATION.md)**
