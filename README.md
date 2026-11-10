# GreenGrow – Organic Farming Awareness and Farmer Guidance Portal

**GreenGrow** is an enterprise-grade agricultural education and farmer guidance web application built with **FastAPI**, **Python 3.11**, and **Oracle Database 23ai** (`FREEPDB1`).

The application is connected with a rural community field survey involving **15 farmers in Tholukodu village**, providing genuine data analytics, organic input estimation, practical agronomic transition guidance, downloadable PDF guides, and a secure administration portal.

---

## Key Features

- **Educational Agronomy Modules**:
  - Principles & definition of organic farming.
  - Soil organic carbon (SOC) and ecological advantages.
  - Balanced analysis of conventional farming risks (product, dose, timing, and management).
  - 9 Detailed Organic Farming Techniques (Composting, Vermicomposting, FYM, Green Manuring, Crop Rotation, Biofertilisers, Mulching, IPM, Biological Control) with procedures, materials, and precautions.
  - Objective Organic vs. Conventional comparison table.
  - Phased transition guidance for smallholder farmers.
- **Input Estimation Calculator**:
  - Computes exact organic manure/compost requirements: `Estimated Quantity = Cultivated Area × Application Rate`.
  - Supports multiple area units (Acres, Hectares, Gunthas, Sq Meters) and rate units (tonnes/acre, kg/acre, etc.).
  - Preserves scientific neutrality: user supplies crop/soil-specific rate without universal assumptions.
- **Farmer Survey Management (Tholukodu Village Field Study)**:
  - Enter, edit, view, and filter genuine farmer questionnaire responses.
  - **Zero Data Fabrication**: Clean slate for primary field research; no fabricated numbers or synthetic percentages.
  - One-click CSV export via **Pandas**.
  - Comprehensive field study PDF report generated dynamically using **ReportLab** with two-pass numbered canvas.
- **Admin Dashboard & Analytics**:
  - Real-time **Chart.js** visualisations (Farming method distribution, input usage, awareness, challenges, willingness, crops, survey timeline).
  - Feedback inbox with status workflow (`New`, `Reviewed`, `Resolved`) and admin notes.
  - Resource manager with secure PDF file upload and download telemetry.
  - Video library management.
  - Role-based admin access control (`superadmin`, `admin`, `editor`) and immutable system audit trail.
- **Bilingual Support**: Instant switcher between **English** and **Telugu (తెలుగు)** with persistent local storage.

---

## Technology Stack

| Layer | Technologies |
|---|---|
| **Backend Framework** | FastAPI 0.110+, Uvicorn (ASGI) |
| **Programming Language** | Python 3.11 |
| **Database Engine** | Oracle Database 23ai Free (Container `oracle23ai`, PDB `FREEPDB1`) |
| **Database Driver** | `python-oracledb` (Thin Mode — Pure Python, zero Instant Client required) |
| **ORM & Migrations** | SQLAlchemy 2.x, Alembic |
| **Frontend UI** | HTML5, CSS3, Bootstrap 5.3, Bootstrap Icons, JavaScript |
| **Analytics Visualisation**| Chart.js |
| **PDF Generation** | ReportLab 4.x / 5.x |
| **Data Processing** | Pandas, OpenPyXL |
| **Authentication & Hash** | JWT (PyJWT), bcrypt (rounds=12), HTTP-only cookies |
| **Test Suite** | pytest, pytest-asyncio, HTTPX / Starlette TestClient |

---

## Step-by-Step macOS Setup Instructions

### 1. Verify Docker is Running
Ensure Docker Desktop is active on your macOS machine:
```bash
docker info
```

### 2. Verify the `oracle23ai` Container
Check that the Oracle Database 23ai container is running:
```bash
docker ps --filter "name=oracle23ai"
```

### 3. Inspect the Exposed Port
Verify the mapped host port (standard listener port is 1521):
```bash
docker port oracle23ai
# Expected output: 1521/tcp -> 0.0.0.0:1521
```

### 4. Verify FREEPDB1 Pluggable Database
Confirm that the pluggable database `FREEPDB1` is open in READ WRITE mode:
```bash
printf "SELECT name, open_mode FROM v\$pdbs;\nEXIT;\n" | docker exec -i oracle23ai sqlplus -s system/Oracle123@FREEPDB1
```

### 5. Create or Configure the Dedicated `greengrow` Database User
Run the setup SQL script as DBA/SYSTEM into `FREEPDB1`:
```bash
docker exec -i oracle23ai sqlplus -s system/Oracle123@FREEPDB1 < database/create_user.sql
```
*Never use the `SYSTEM` account for application queries. The dedicated `greengrow` user is granted `CREATE SESSION`, `CREATE TABLE`, `CREATE SEQUENCE`, `CREATE VIEW`, and unlimited quota on the `USERS` tablespace.*

### 6. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Default parameters in `.env`:
```env
ORACLE_USER=greengrow
ORACLE_PASSWORD=greengrow
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=FREEPDB1

SECRET_KEY=greengrow-organic-portal-super-secret-key-2026-production-ready
JWT_SECRET_KEY=greengrow-jwt-token-signing-secret-key-2026-secure-vault
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

APP_NAME=GreenGrow
APP_ENV=development
DEBUG=True
HOST=127.0.0.1
PORT=8000
```

### 7. Create a Python Virtual Environment
Use Python 3.11 to create an isolated environment:
```bash
/opt/homebrew/bin/python3.11 -m venv .venv
source .venv/bin/activate
```

### 8. Install Python Dependencies
Install all required libraries:
```bash
pip install -r backend/requirements.txt
```

### 9. Run Alembic Database Migrations
Apply the initial schema to Oracle Database 23ai:
```bash
alembic upgrade head
```

### 10. Verify Oracle Database Connection
Run the connection verification script to confirm Thin Mode connectivity:
```bash
python backend/scripts/test_db_connection.py
```

### 11. Seed Initial Educational Content & Admin Account
Populate default educational categories, articles, FAQs, videos, and create the default superadmin account:
```bash
python backend/scripts/seed_initial_data.py
```
*Note: Farmer survey records are left at 0 for genuine owner data entry.*

### 12. Start the FastAPI Application Server
From the workspace root:
```bash
source .venv/bin/activate
PYTHONPATH=backend uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

## Application URLs & Credentials

| Resource | URL |
|---|---|
| **Public Web Portal** | [http://127.0.0.1:8000](http://127.0.0.1:8000) |
| **Interactive OpenAPI Documentation** | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) |
| **ReDoc API Specifications** | [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) |
| **System & Oracle Health Endpoint** | [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) |
| **Admin Portal Login** | [http://127.0.0.1:8000/admin/login](http://127.0.0.1:8000/admin/login) |

### Default Administrator Credentials
- **Username**: `admin`
- **Password**: `AdminPass123!`
- **Role**: `superadmin`

---

## Running Automated Tests

Run the full automated test suite covering authentication, Oracle connection, CRUD operations, survey validations, ReportLab PDF generation, CSV streaming, and calculator mathematics:
```bash
source .venv/bin/activate
pytest backend/tests/ -v
```

All 17 automated tests run directly against Oracle Database 23ai (`FREEPDB1`). No SQLite fallback is used.

---

## Database Backup & Export

Run the automated backup script to capture database table manifests and record counts:
```bash
bash backend/scripts/backup_db.sh
```

---

## Project Structure

```
GreenGrow/
├── backend/
│   ├── app/
│   │   ├── main.py                  # Application entry point & middleware
│   │   ├── core/
│   │   │   ├── config.py            # Pydantic v2 settings & URL builder
│   │   │   ├── security.py          # bcrypt hashing & JWT tokens
│   │   │   └── dependencies.py      # Auth & superadmin guards
│   │   ├── database/
│   │   │   ├── connection.py        # SQLAlchemy engine & session pool
│   │   │   └── base.py              # DeclarativeBase model foundation
│   │   ├── models/                  # 11 Oracle SQLAlchemy ORM models
│   │   ├── schemas/                 # Pydantic v2 validation contracts
│   │   ├── services/                # Analytics, PDF, CSV, calculator services
│   │   ├── routers/                 # Public web pages & REST API routers
│   │   ├── templates/               # Jinja2 templates (Public & Admin)
│   │   └── static/                  # CSS, JS, translation files
│   ├── migrations/                  # Alembic migration scripts
│   ├── scripts/                     # Seeders, test scripts, backup utilities
│   ├── tests/                       # 17 Automated pytest & HTTPX tests
│   └── requirements.txt             # Production dependency manifest
├── database/
│   ├── create_user.sql              # Oracle user creation & grants script
│   └── setup_notes.md               # Oracle container connectivity details
├── uploads/                         # Safe uploads directory (.gitkeep)
│   ├── resources/
│   └── articles/
├── docs/
│   └── architecture.md              # System architecture blueprint
├── alembic.ini                      # Migration configuration
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore rules
└── README.md                        # Documentation
```
