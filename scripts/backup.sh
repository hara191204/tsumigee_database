#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
COMPOSE_FILE="$PROJECT_DIR/docker-compose.prod.yml"
ENV_FILE="$PROJECT_DIR/.env"
BACKUP_DIR="${BACKUP_DIR:-/home/hara/backups}"
KEEP_DAYS=30

CSV_TABLES=(
  tsumigee_database_game
  tsumigee_database_maker
  tsumigee_database_hard
)

# .env から接続情報を読み込む
if [[ ! -f "$ENV_FILE" ]]; then
  echo "[backup] ERROR: .env not found at $ENV_FILE" >&2
  exit 1
fi
# shellcheck disable=SC1090
source "$ENV_FILE"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/tsumigee_${TIMESTAMP}.sql"
CSV_DIR="$BACKUP_DIR/csv_${TIMESTAMP}"

mkdir -p "$BACKUP_DIR" "$CSV_DIR"

# --- SQL ダンプ ---
echo "[backup] Starting dump → $BACKUP_FILE"
docker compose -f "$COMPOSE_FILE" exec -T db \
  mysqldump -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" \
  > "$BACKUP_FILE"
echo "[backup] Done. Size: $(du -h "$BACKUP_FILE" | cut -f1)"

# --- CSV エクスポート ---
echo "[backup] Exporting CSV → $CSV_DIR"
for table in "${CSV_TABLES[@]}"; do
  docker compose -f "$COMPOSE_FILE" exec -T db \
    mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" \
    --default-character-set=utf8mb4 --batch -e "SELECT * FROM \`${table}\`" \
    | awk -F'\t' '{
        for (i = 1; i <= NF; i++) {
          gsub(/"/, "\"\"", $i)
          printf "\"%s\"", $i
          if (i < NF) printf ","
        }
        print ""
      }' > "$CSV_DIR/${table}.csv"
  echo "[backup]   ${table}.csv ($(wc -l < "$CSV_DIR/${table}.csv") rows)"
done

# --- 古いバックアップを削除 ---
find "$BACKUP_DIR" -name "tsumigee_*.sql" -mtime +"$KEEP_DAYS" -delete
find "$BACKUP_DIR" -maxdepth 1 -name "csv_*" -type d -mtime +"$KEEP_DAYS" \
  -exec rm -rf {} +
echo "[backup] Deleted backups older than ${KEEP_DAYS} days."
