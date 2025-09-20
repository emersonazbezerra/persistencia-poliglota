# persistencia-poliglota

This project includes a Docker Compose setup for running MongoDB and Mongo Express for database management.

## Getting Started with Docker

### Prerequisites
- Docker and Docker Compose installed on your system

### Running the Services

1. Start the MongoDB and Mongo Express services:
```bash
docker compose up -d
```

2. Access the services:
   - **MongoDB**: Available on `localhost:27017`
   - **Mongo Express** (Web UI): Available on `http://localhost:8081`

### Default Configuration

- **MongoDB**:
  - Username: `admin`
  - Password: `password123`
  - Database: `persistencia_poliglota`
  - Port: `27017`

- **Mongo Express**:
  - Port: `8081`
  - No authentication required (disabled for development)

### Managing the Services

- Stop services: `docker compose down`
- View logs: `docker compose logs`
- Remove volumes (data will be lost): `docker compose down -v`

### Data Persistence

MongoDB data is persisted in Docker volumes, so your data will survive container restarts. The volumes created are:
- `persistencia-poliglota_mongodb_data`: Database files
- `persistencia-poliglota_mongodb_config`: Configuration files