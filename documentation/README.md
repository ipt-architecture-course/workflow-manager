# Workflow Manager

The **Workflow Manager** is a service designed to orchestrate content workflows by interacting with various external services like **Profile Manager**, **Thumbnail Generator**, **Keywords Generator**, **ChatGPT**, and others. It uses the **Hexagonal Architecture (Ports & Adapters)** pattern to ensure scalability, extensibility, and maintainability.

---

## 📖 What is the Workflow Manager?

The Workflow Manager acts as the central component of a distributed system designed to process user content dynamically. It:
- Determines the required processing based on user profiles.
- Orchestrates external services to execute specific tasks (e.g., generate thumbnails or extract keywords).
- Tracks the progress of workflows and provides status updates to clients.
- Supports both synchronous and asynchronous communication via **REST** and **RabbitMQ**.

---

## ✨ Key Features

- **Dynamic Orchestration:** Automatically determines the required processing steps based on user profiles.
- **Extensibility:** New adapters for third-party services can be added seamlessly.
- **Scalability:** Asynchronous messaging with RabbitMQ ensures high performance.
- **Ease of Use:** Developer-friendly REST APIs for interaction.
- **Modular Architecture:** Implements the Hexagonal Architecture for clear separation of concerns.

---

## 📚 Documentation
Purpose of Each API
1. Workflow Manager API
The central API provides endpoints for:

Starting a workflow.
Checking the status of workflows.
2. Profile Manager API
Determines the type of processing required for a user profile. Communication is synchronous (REST).

3. RabbitMQ Topics
Handles asynchronous communication between the Workflow Manager and external services:

Request Topics: To send processing requests.
Response Topics: To receive results from external services.
4. External Services
External services process specific tasks:

Thumbnail Generator: Creates thumbnails for uploaded content.
Keywords Generator: Extracts keywords from text-based content.
ChatGPT Integration: Summarizes or transforms text dynamically.
## 🔄 Communication Flow
1. Starting a Workflow
Input: The Workflow Manager receives a request:
json
Copiar código
{
  "id_profile": "123",
  "id_conteudo": "456"
}
Profile Manager Communication: The Workflow Manager queries the Profile Manager to identify the process_type:
json
Copiar código
{
  "id_profile": "123",
  "process_type": "thumbnail"
}
Processing Request: Based on the process_type, the Workflow Manager publishes a message to RabbitMQ:
json
Copiar código
{
  "workflow_id": "abc-123",
  "id_conteudo": "456"
}
2. Processing and Results
Request: The Workflow Manager publishes processing requests to RabbitMQ on topics like generator.thumbnail.process.
Response: External services publish results back to a common topic workflow.results:
json
Copiar código
{
  "workflow_id": "abc-123",
  "status": "completed",
  "output": {
    "url": "https://example.com/thumbnail.jpg"
  }
}
🚀 Getting Started
Prerequisites
Python 3.9+
RabbitMQ instance (local or cloud)
Profile Manager service running (for production setups)
Installation
Clone the Repository:

bash
Copiar código
git clone https://github.com/ipt-architecture-course/workflow-manager.git
cd workflow-manager
Set Up a Virtual Environment:

bash
Copiar código
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:

bash
Copiar código
pip install -r requirements.txt
Run the Application:

bash
Copiar código
uvicorn app.main:app --reload
🔧 Adding New Adapters
Implement the BaseAdapter Interface:

python
Copiar código
from app.ports.base_adapter import BaseAdapter

class NewAdapter(BaseAdapter):
    def process(self, workflow_id: str, id_conteudo: str):
        print(f"Processing {workflow_id} with content {id_conteudo}")
Register the Adapter in adapters_config.json:

json
Copiar código
{
    "new_process_type": "app.adapters.new_adapter.NewAdapter"
}
## 🌐 API Endpoints
1. Start a Workflow
Endpoint: POST /workflows/start
Request Payload:

json
Copiar código
{
  "id_profile": "123",
  "id_conteudo": "456"
}
Response:

json
Copiar código
{
  "workflow_id": "abc-123",
  "status": "processing_started"
}
2. Check Workflow Status
Endpoint: GET /workflows/status/{workflow_id}
Response:

json
Copiar código
{
  "workflow_id": "abc-123",
  "status": "completed",
  "results": {
    "thumbnail": "https://example.com/thumbnail.jpg"
  }
}
## 🧪 Testing
Run Unit Tests
To execute all tests:

bash
Copiar código
pytest

## 🗂️ Project Structure

```plaintext
workflow-manager/
├── app/
│   ├── __init__.py
│   ├── main.py                # Entry point for the application
│   ├── controllers/           # REST API layer
│   │   ├── __init__.py
│   │   ├── workflow_controller.py
│   ├── core/                  # Business logic layer
│   │   ├── __init__.py
│   │   ├── workflow_service.py
│   │   ├── processor_factory.py
│   ├── ports/                 # Interface definitions for external communication
│   │   ├── __init__.py
│   │   ├── base_adapter.py    # Generic adapter interface
│   ├── adapters/              # Implementations of adapters
│   │   ├── __init__.py
│   │   ├── profile_adapter.py
│   │   ├── rabbitmq_adapter.py
│   │   ├── thumbnail_adapter.py
│   │   ├── keywords_adapter.py
│   │   ├── chatgpt_adapter.py
│   ├── utils/                 # Utility functions
│   │   ├── __init__.py
│   │   ├── config_loader.py
├── adapters_config.json       # Configuration file for registering adapters
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation

