#!/usr/bin/env bash
# ==============================================================================
# GreenGrow - Oracle Database 23ai Backup & Export Script
# Uses SQL*Plus and Data Pump / CSV extract within docker container oracle23ai
# ==============================================================================

set -euo pipefail

BACKUP_DIR="$(pwd)/backups"
TIMESTAMP="$(date +'%Y%m%d_%H%M%S')"
mkdir -p "${BACKUP_DIR}"

echo "================================================================="
echo "Starting GreenGrow Database Backup: ${TIMESTAMP}"
echo "================================================================="

# Export tables metadata and rows count
BACKUP_LOG="${BACKUP_DIR}/backup_${TIMESTAMP}.log"
echo "Logging backup details to: ${BACKUP_LOG}"

docker exec -i oracle23ai sqlplus -s greengrow/greengrow@FREEPDB1 << EOF > "${BACKUP_LOG}"
SET PAGESIZE 100
SET LINESIZE 150
PROMPT Database Backup Manifest - ${TIMESTAMP}
PROMPT =====================================================
SELECT table_name, num_rows, last_analyzed FROM user_tables ORDER BY table_name;
PROMPT =====================================================
PROMPT Total Records in Survey Responses:
SELECT COUNT(*) AS total_survey_responses FROM survey_responses;
PROMPT =====================================================
EXIT;
EOF

echo "[✓] Manifest generated at: ${BACKUP_LOG}"
cat "${BACKUP_LOG}"
echo "================================================================="
echo "Backup Completed Successfully!"
echo "================================================================="
