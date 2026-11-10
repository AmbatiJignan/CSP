# GreenGrow Database Setup Notes

## Oracle Database 23ai Container Environment
- **Docker Container**: `oracle23ai`
- **Host Port Mapping**: `1521` (TCP mapped to `0.0.0.0:1521` and `[::]:1521`)
- **PDB Service Name**: `FREEPDB1`
- **Application User**: `greengrow`
- **Application Password**: `greengrow` (or configured via `ORACLE_PASSWORD` in `.env`)
- **Default Tablespace**: `USERS` (Unlimited Quota)
- **Temporary Tablespace**: `TEMP`

## Database Connection Details
- Driver: `python-oracledb` in Thin mode (pure Python, does not require Oracle Instant Client).
- Dialect: `oracle+oracledb`
- SQLAlchemy URL format: `oracle+oracledb://greengrow:greengrow@localhost:1521/?service_name=FREEPDB1`
- Connection health check: `SELECT 1 FROM DUAL`

## Creating / Resetting the Schema User
To run the setup script via SQL*Plus inside the Docker container:
```bash
docker exec -i oracle23ai sqlplus system/Oracle123@FREEPDB1 < database/create_user.sql
```

## Running Alembic Migrations
```bash
source .venv/bin/activate
alembic upgrade head
```
