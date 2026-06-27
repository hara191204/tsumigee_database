#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
COMPOSE_FILE="$PROJECT_DIR/docker-compose.prod.yml"
ENV_FILE="$PROJECT_DIR/.env"
BACKUP_DIR="${BACKUP_DIR:-/home/hara/backups}"
KEEP_DAYS=30

# .env から接続情報を読み込む
if [[ ! -f "$ENV_FILE" ]]; then
  echo "[backup] ERROR: .env not found at $ENV_FILE" >&2
  exit 1
fi
# shellcheck disable=SC1090
source "$ENV_FILE"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/tsumigee_${TIMESTAMP}.sql"

mkdir -p "$BACKUP_DIR"

echo "[backup] Starting dump → $BACKUP_FILE"
docker compose -f "$COMPOSE_FILE" exec -T db \
  mysqldump -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" \
  > "$BACKUP_FILE"

echo "[backup] Done. Size: $(du -h "$BACKUP_FILE" | cut -f1)"

# 古いバックアップを削除
find "$BACKUP_DIR" -name "tsumigee_*.sql" -mtime +"$KEEP_DAYS" -delete
echo "[backup] Deleted backups older than ${KEEP_DAYS} days."
