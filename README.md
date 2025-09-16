# Serverless Function Execution Platform  
*A platform to deploy & execute functions on‑demand (via HTTP), support multiple languages (Python, JavaScript), enforce constraints, use virtualization techs (Docker + Firecracker / Unikernel / gVisor etc.), with monitoring dashboard*

---

## Table of Contents

1. High Level Design (HLD)  
   1.1. Overview  
   1.2. System Architecture  
   1.3. Component Breakdown  
   1.4. Technology Stack  
   1.5. Non‑Functional Requirements & Constraints  
   1.6. Data Flow & Sequence  
   1.7. Trade‑offs / Design Decisions  

2. Low Level Design (LLD)  
   2.1. Module Specifications  
   2.2. API Definitions  
   2.3. Data Models / Database Schema  
   2.4. Execution Engine Details  
   2.5. Virtualization Components Design  
   2.6. Monitoring / Metrics Design  
   2.7. Error handling, Timeouts, Security  
   2.8. CI/CD / Deployment Design  

3. Getting Started / Setup Instructions  

4. Project Structure  

5. Future Enhancements (Optional)  

6. Contributors  

---

## 1. High Level Design (HLD)

### 1.1 Overview  
- Goal: Provide HTTP interface for users to deploy, run, and monitor functions in Python & JavaScript, with execution constraints (timeout, resource usage).  
- Support two virtualization technologies (Docker + one of Firecracker / gVisor / Unikernel) for performance comparison.  
- Provide front end dashboard to monitor request volume, response times, error rates, resource utilization.  

### 1.2 System Architecture  
- **Frontend**: Web UI for users to:  
    • Submit functions (code, metadata)  
    • Manage existing functions (list/update/delete)  
    • View metrics / dashboard  

- **Backend API Server**:  
    • CRUD for function metadata  
    • Endpoint to receive HTTP request to run a function  

- **Execution Engine(s)**:  
    • Docker-based containers (pre‑warmed or pooled)  
    • Second virtualization approach (e.g., Firecracker MicroVMs)  

- **Monitoring / Metrics subsystem**:  
    • Instrumentation of execution (latency, errors, resource usage)  
    • Aggregation and storage of metrics  

- **Data Storage**:  
    • Metadata DB (for function info, versions, settings)  
    • Metrics DB (for monitoring)  

- **CI/CD Pipeline**: automation of build, testing, deployment  

### 1.3 Component Breakdown  

| Component | Responsibility |
|---|---|
| API Gateway / HTTP Router | Route incoming HTTP requests to frontend or to proper execution API |
| Function Manager | Handle function upload, update, delete, metadata, versioning, packaging |
| Execution Coordinator | Decide which virtualization path to use; manage resource limits / timeouts |
| Container Manager / VM Manager | Manage pools of containers or VMs, pre‑warming, start‑stop, isolation |
| Metrics Collector | Capture execution time, error rate, usage stats |
| Dashboard Service | Visualize metrics (charts, graphs) per function and system‑wide |
| Authentication/Authorization (if implemented) | Secure endpoints, restrict access |

### 1.4 Technology Stack  

- **Backend**: probably use **FastAPI** (Python) or **Express.js** (Node.js)  
- **Virtualization**: Docker + Firecracker or gVisor etc.  
- **Database**: PostgreSQL or MySQL for metadata; maybe a time‑series DB or something like Prometheus / InfluxDB for metrics  
- **Frontend**: Use ReactJS / Streamlit / Vue / some dashboard framework  
- **Infrastructure**: Container orchestration or lightweight VM management; possibly using Docker Compose, Kubernetes (optional)  
- **CI/CD**: GitHub Actions / Jenkins / GitLab CI  

### 1.5 Non‑Functional Requirements & Constraints  

- **Timeouts**: enforce max execution time per function invocation  
- **Resource limits**: CPU / memory / disk usage limits per function  
- **Scalability**: ability to handle multiple concurrent executions; pre‑warming to reduce cold start latency  
- **Language support**: at least Python & JavaScript; clean isolation between environments  
- **Security**: isolation; prevent malicious code; limit resource abuse; sanitization if needed  
- **Monitoring / Observability**: real‑time metrics; dashboards; logging of errors  

### 1.6 Data Flow & Sequence  

1. User uploads function via frontend → metadata stored, code packaged  
2. User triggers function via HTTP API → request enters router  
3. Execution Coordinator selects virtualization path and instance (container or VM)  
4. Code executes inside environment with enforced limits  
5. Result or error returned to user  
6. Metrics captured: response time, success/failure, resource usage  
7. Dashboard updated  

### 1.7 Trade‑offs / Design Decisions  

- Using Docker vs Firecracker: containers are faster to start; microVMs might give stronger isolation at cost of overhead  
- Pre‑warm vs cold start: pre‑warming helps latency; but uses more resources  
- Choosing metrics DB: time series DB gives better performance vs just relational DB  
- How strict to be on security: sandboxing etc  

---

## 2. Low Level Design (LLD)

### 2.1 Module Specifications  

- **Function Manager Module**:  
    • **Upload Function**: input: code, metadata (language, timeout, memory), version → stores to storage, builds package  
    • **Update Function**: change code or metadata; versioning  
    • **Delete Function**: remove package, clean up environments, metadata  

- **Execution Module**:  
    • Entry point for execution requests  
    • Validation (language, resource constraints)  
    • Routing to virtualization backend  
    • Container / VM start or reuse (warm pool)  
    • Timeout control  

- **Container Backend**:  
    • Base images for Python & JS  
    • Packaging code into image or mounting code  
    • Resource limits (Docker CPU/memory)  

- **Second Virtualization Backend** (e.g. Firecracker):  
    • Setup microVM images or snapshots  
    • Similar packaging / interface to Execution Module  

- **Metrics Module**:  
    • Capture start & end times, status (success/error), CPU/memory usage  
    • Logging system for each invocation  

- **Dashboard Module**:  
    • Frontend endpoints to fetch metrics (per function, system wide)  
    • Graphs / charts (e.g., request per minute / error rate over time)  

- **Auth Module** (if included):  
    • Login endpoints or token system  
    • Permissions: who can deploy / view metrics etc  

### 2.2 API Definitions  

| Endpoint | Method | Request | Response | Description |
|---|---|---|---|---|
| `/functions` | POST | `{ name, language, timeout, code (or code upload) }` | `{ id, version, status }` | Deploy / create new function |
| `/functions/{id}` | GET | — | Function metadata |
| `/functions/{id}` | PUT | Updated metadata or new code | Updated info |
| `/functions/{id}` | DELETE | — | Delete function |
| `/execute/{id}` | POST | `{ input, parameters }` | `{ output or error }` |
| `/metrics/functions/{id}` | GET | time range etc | metrics data points |
| `/metrics/system` | GET | time range etc | aggregated metrics |

### 2.3 Data Models / Database Schema  

**Function metadata table**  
- `function_id` (PK)  
- `name`  
- `language`  
- `timeout_ms`  
- `memory_limit_mb`  
- `created_at`  
- `updated_at`  
- `version`  
- `status`  

**Metrics table**  
- `metric_id` (PK)  
- `function_id` (FK)  
- `request_timestamp`  
- `response_time_ms`  
- `error_flag` / `error_message`  
- `cpu_usage`  
- `memory_usage`  

Other tables: users / auth (if needed)

### 2.4 Execution Engine Details  

- Warm pool vs on‑demand: maintain a pool of docker containers / microVMs ready for each language  
- Timeout enforcement: use host OS controls + Docker / VM settings to limit execution time; also kill processes if they exceed limit  
- Packaging: for Docker, build images or mount code; for Firecracker / microVM, perhaps snapshot approach + lightweight bootstrap  

### 2.5 Virtualization Components Design  

- Docker backend: base images, network isolation, resource constraints via Docker engine  
- Firecracker (or other microVM): how to manage microVM lifecycle, snapshot vs cold boot, triggering instance, how to handle code injection or mounting code  

### 2.6 Monitoring / Metrics Design  

- Use middleware / wrapper around execution to capture timing, start & end, memory & CPU metrics  
- Logging: levels (info, error), store logs per invocation  
- Aggregation: hourly / daily / function‑wise summaries  

### 2.7 Error Handling, Timeouts, Security  

- Validate inputs early (language, size limits)  
- Catch runtime errors; return meaningful error responses  
- Sanitize user code (as much as possible)  
- Use sandboxing / isolation to prevent one function from destroying / affecting others  

### 2.8 CI/CD / Deployment Design  

- GitHub repository structure: backend, frontend, execution engines etc  
- Automated testing: unit tests (for API, exec logic), integration tests  
- CI: on commit, run tests, build containers / VM artifacts, lint, etc  
- Deployment: perhaps use Docker Compose or scripts to deploy backend + front end + exec engines locally / dev  

---

## 3. Getting Started / Setup Instructions

```bash
# Clone repo
git clone <repo‑url>  
cd serverless‑platform  

# Backend setup  
cd backend  
pip install ‑r requirements.txt   # or npm install  
# Setup DB (create schema etc)  

# Execution engines  
cd execution/docker  
# Build base images etc  

# Frontend setup  
cd frontend  
npm install / streamlit setup  

# Run local environment  
docker compose up   # if using compose, else scripts  

# Run tests  
pytest / npm test etc  
