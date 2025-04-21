# Age Groups API  

A simple CRUD microservice for managing age groups, built with FastAPI and MongoDB.  
It can be used standalone or in conjunction with the [Enrollment API](https://github.com/itsmevicot/enrollment_api)
to validate and process enrollments based on age ranges.

---

## Overview

- **Framework:** FastAPI  
- **Database:** MongoDB (uses `mongomock` in tests)  
- **Pattern:** Dependency Injection via FastAPI `Depends`  
- **Testing:** Comprehensive pytest suite with automatic cleanup  

## Integration with Enrollment API

The [Enrollment API](https://github.com/itsmevicot/enrollment_api) publishes new enrollments to a RabbitMQ queue.  
The Enrollment Worker then calls this Age Groups API to retrieve the current buckets and determine acceptance or rejection.  

1. **Enrollment Service** posts to `/enrollments/` and enqueues a message.  
2. **Enrollment Worker** consumes the queue and calls `GET /age-groups/` on this service.  
3. **Age Groups API** returns defined age brackets, which drive the acceptance logic.

---

## Prerequisites

- Python 3.10+  
- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/) (optional)

## Installation

```bash
git clone https://github.com/itsmevicot/age_groups_api.git
cd age_groups_api
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate     # Windows
pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

Copy the sample environment file:

```bash
cp .env.example .env
```

Edit `.env` to suit your environment, e.g.: 

```dotenv
PORT=8000
MONGO_URI=mongodb://mongo:27017/age_groups_db
MONGO_DB_NAME=age_groups_db
```  

When working with the Enrollment API, also set `CORS_ORIGINS` or `AGE_GROUPS_API_URL` accordingly.

## Running the API

### 1. Without Docker

```bash
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --reload
```

Open `http://localhost:${PORT}/docs` for Swagger UI.

### 2. With Docker Compose

```bash
docker-compose up -d
```  

Follow logs:

```bash
docker-compose logs -f api
```  

Stop services:

```bash
docker-compose down
```  

## API Endpoints

| Method | Path               | Description                  |
|--------|--------------------|------------------------------|
| POST   | `/age-groups/`     | Create a new age group       |
| GET    | `/age-groups/`     | List all age groups          |
| GET    | `/age-groups/{id}` | Retrieve a group by ID       |
| DELETE | `/age-groups/{id}` | Delete a group by ID         |

### Example Usage

```bash
# Create group
curl -X POST http://localhost:8000/age-groups/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Kids","min_age":0,"max_age":12}'

# List
curl http://localhost:8000/age-groups/

# Get
curl http://localhost:8000/age-groups/{id}

# Delete
curl -X DELETE http://localhost:8000/age-groups/{id}
```

---

## Testing

Runs entirely in-memory with `mongomock`:

```bash
pytest
```  

Or inside Docker:

```bash
docker-compose exec api pytest
```
