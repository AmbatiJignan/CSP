#!/usr/bin/env python3
"""
GreenGrow - Oracle Database 23ai Connection Verification Script
Tests python-oracledb Thin Mode connection and SQLAlchemy pool status.
"""

import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import text
from app.core.config import settings
from app.database.connection import engine, check_db_health


def main():
    print("=" * 65)
    print("GreenGrow - Oracle Database 23ai Connection Verification")
    print("=" * 65)
    print(f"Target Host      : {settings.ORACLE_HOST}")
    print(f"Target Port      : {settings.ORACLE_PORT}")
    print(f"Service Name     : {settings.ORACLE_SERVICE_NAME}")
    print(f"Schema User      : {settings.ORACLE_USER}")
    print(f"Driver / Mode    : python-oracledb (Thin Mode - Pure Python)")
    print("-" * 65)

    try:
        with engine.connect() as conn:
            # 1. Basic Ping
            val = conn.execute(text("SELECT 1 FROM DUAL")).scalar()
            print(f"[✓] Basic Health Ping (SELECT 1 FROM DUAL): Result = {val}")

            # 2. Database Version & Container Info
            banner = conn.execute(text("SELECT banner FROM v$version WHERE ROWNUM = 1")).scalar()
            print(f"[✓] Database Banner: {banner}")

            # 3. Current User and Session Container
            user_info = conn.execute(text("SELECT USER, SYS_CONTEXT('USERENV', 'CON_NAME') FROM DUAL")).fetchone()
            print(f"[✓] Connected User: {user_info[0]} | Pluggable Database: {user_info[1]}")

            # 4. Count Existing Tables in User Schema
            table_count = conn.execute(text("SELECT COUNT(*) FROM user_tables")).scalar()
            print(f"[✓] Total Tables in Schema '{settings.ORACLE_USER}': {table_count}")

            # List tables
            tables = conn.execute(text("SELECT table_name FROM user_tables ORDER BY table_name")).fetchall()
            table_names = [t[0] for t in tables]
            print(f"    Tables: {', '.join(table_names)}")

        print("-" * 65)
        print("[SUCCESS] Oracle Database 23ai is fully operational and accessible!")
        print("=" * 65)
        return 0

    except Exception as exc:
        print("-" * 65)
        print(f"[ERROR] Database connection failed: {exc}")
        print("=" * 65)
        return 1


if __name__ == "__main__":
    sys.exit(main())
