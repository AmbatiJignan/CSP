# GreenGrow System Architecture Documentation

## 1. Executive Architecture Summary

GreenGrow is an enterprise-grade full-stack web application designed for agricultural education, organic farming transition advisory, and community field research analytics. The system integrates a high-performance **FastAPI** Python application server with a containerised **Oracle Database 23ai** instance (`FREEPDB1`) running through pure Python `python-oracledb` Thin mode.

```
+-------------------------------------------------------------------------------+
|                               Presentation Layer                              |
|   - Responsive HTML5 & CSS3 Bootstrap 5.3 Interface                          |
|   - Bilingual Interface (English & Telugu dynamic switcher)                   |
|   - Interactive Chart.js Visualisations (Strictly Real Data)                  |
|   - Reactive Input Estimation Calculator                                      |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
|                                   API Layer                                   |
|   - FastAPI REST API Endpoints (/api/v1/...)                                  |
|   - Pydantic v2 Request & Response Validation Schemas                         |
|   - JWT (HS256) Bearer Authentication & Cookie Session Support                |
|   - Role-Based Access Control (Superadmin, Admin, Editor)                     |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
|                              Business Logic Layer                             |
|   - Farmer Survey Validation & Record Service                                 |
|   - Actual Data Analytics Aggregation Service                                 |
|   - ReportLab Two-Pass Numbered Canvas PDF Generation Engine                  |
|   - Pandas CSV Export Pipeline                                                |
|   - System Audit Trail Logging Service                                        |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
|                              Data Access Layer                                |
|   - SQLAlchemy 2.x Declarative ORM Models                                     |
|   - Alembic Migration Engine for Oracle DDL Versioning                        |
|   - Connection Pool with Health Ping (pool_pre_ping=True)                     |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
|                         Oracle Database 23ai (Docker)                         |
|   - Container: oracle23ai (PDB: FREEPDB1)                                     |
|   - Driver: python-oracledb (Thin Mode - Pure Python)                         |
|   - Schema: Dedicated 'greengrow' User                                        |
+-------------------------------------------------------------------------------+
```

---

## 2. Database Schema Design (Oracle 23ai)

The relational schema is fully normalized into 11 Oracle tables:

1. **`ADMIN_USERS`**: Secure administrative accounts with bcrypt-hashed credentials, roles (`superadmin`, `admin`, `editor`), and activity flags.
2. **`ARTICLE_CATEGORIES`**: Taxonomy for educational guides and articles.
3. **`ARTICLES`**: Long-form educational articles, summaries, author tracking, view counters, and publication state.
4. **`FAQS`**: Categorised frequently asked questions and answers with display ordering.
5. **`RESOURCES`**: Downloadable PDF guides, government scheme circulars, and technical manuals with download telemetry.
6. **`FEEDBACK`**: Farmer inquiries and public feedback with workflow statuses (`New`, `Reviewed`, `Resolved`) and admin notes.
7. **`SURVEY_RESPONSES`**: Primary field survey records from Tholukodu village (respondent code, farming method, crops, awareness, challenges, willingness, date, verbal consent).
8. **`EDUCATIONAL_VIDEOS`**: Curated practical demonstration videos with category and duration tags.
9. **`ANNOUNCEMENTS`**: High-priority seasonal agricultural alerts and research updates.
10. **`AUDIT_LOGS`**: Immutable audit logs capturing user actions, target entities, IP addresses, and timestamps.
11. **`ALEMBIC_VERSION`**: Schema migration version tracking table.

---

## 3. Security Architecture

- **Password Hashing**: Direct `bcrypt` hashing with salt rounds = 12.
- **Authentication**: Stateless JSON Web Tokens (JWT) signed with HS256, supported in both `Authorization: Bearer <token>` HTTP headers and secure HTTP-only browser cookies for seamless dashboard interactions.
- **Role-Based Access Control**: Route-level dependencies (`require_superadmin`, `get_current_admin`).
- **Input Validation**: Strict Pydantic v2 schemas validating positive values, email formats, and string lengths.
- **Database Safety**: Principle of least privilege using a dedicated schema user `greengrow`. Passwords escaped via SQLAlchemy `URL.create`.
- **Upload Hygiene**: Restrict file extensions to `.pdf, .doc, .docx, .xlsx, .txt`, enforce a 15MB file size ceiling, and use UUID-prefixed safe filenames.
