# Distributed Task Queue (DTQ)

DTQ is a modular, high-performance distributed task queue designed for asynchronous background processing. It supports pluggable brokers and result backends.

## 🏗️ Architecture
- **Core Engine**: Orchestrates task execution and retries.
- **Brokers**: Pluggable transport layers (AMQP, Redis, etc.).
- **Storage**: Persistent storage for task metadata and results.
- **API**: A monitoring interface to track task status.

## 🚀 Features
- Task scheduling and prioritization.
- Automatic retries with exponential backoff.
- Multi-broker support (currently AMQP).

## 🚧 Unfinished Work (Priority)
- **Redis Broker**: Implement the `RedisBroker` class in `src/brokers/redis.py`.
- **Dead Letter Queue (DLQ)**: Implement logic to move repeatedly failing tasks to a DLQ.
- **API Dash**: Complete the `/stats` endpoint in the FastAPI monitoring API.
- **CLI**: Create a `dtq-cli` for managing tasks from the terminal.
