-- ==============================================================================
-- GreenGrow - Dedicated Application User & Schema Setup Script
-- Database: Oracle Database 23ai (PDB: FREEPDB1)
-- Run this script as SYSTEM or a DBA user connected to FREEPDB1:
--   docker exec -i oracle23ai sqlplus system/Oracle123@FREEPDB1 < database/create_user.sql
-- ==============================================================================

-- 1. Ensure we are in the pluggable database FREEPDB1
ALTER SESSION SET CONTAINER = FREEPDB1;

-- 2. Create or verify the dedicated application user
DECLARE
    user_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO user_count FROM all_users WHERE username = 'GREENGROW';
    IF user_count = 0 THEN
        EXECUTE IMMEDIATE 'CREATE USER greengrow IDENTIFIED BY "greengrow" DEFAULT TABLESPACE users TEMPORARY TABLESPACE temp QUOTA UNLIMITED ON users';
        DBMS_OUTPUT.PUT_LINE('User GREENGROW created successfully.');
    ELSE
        EXECUTE IMMEDIATE 'ALTER USER greengrow IDENTIFIED BY "greengrow" DEFAULT TABLESPACE users TEMPORARY TABLESPACE temp QUOTA UNLIMITED ON users ACCOUNT UNLOCK';
        DBMS_OUTPUT.PUT_LINE('User GREENGROW already exists; password and quota verified.');
    END IF;
END;
/

-- 3. Grant essential application privileges (principle of least privilege)
GRANT CREATE SESSION TO greengrow;
GRANT CREATE TABLE TO greengrow;
GRANT CREATE SEQUENCE TO greengrow;
GRANT CREATE VIEW TO greengrow;
GRANT CREATE TRIGGER TO greengrow;
GRANT CREATE PROCEDURE TO greengrow;

-- 4. Verify user privileges and quota
PROMPT ===================================================
PROMPT Verification of GREENGROW User Privileges:
PROMPT ===================================================
SELECT privilege FROM dba_sys_privs WHERE grantee = 'GREENGROW' ORDER BY privilege;

PROMPT ===================================================
PROMPT Verification of Tablespace Quota:
PROMPT ===================================================
SELECT tablespace_name, bytes, max_bytes FROM dba_ts_quotas WHERE username = 'GREENGROW';

PROMPT ===================================================
PROMPT Setup Complete!
PROMPT ===================================================
EXIT;
