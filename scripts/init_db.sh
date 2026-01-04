#!/bin/bash
set -e

DB_HOST="giniewicz.it"
DB_PORT="3306"
DB_NAME="team05"
DB_USER="team05"
DROP_SCRIPT="../database/seeds/dev/drop_db.sql"

cleanup_on_error() {
    echo "ERROR: Process failed!"
    if [ -f "$DROP_SCRIPT" ]; then
        mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" "$DB_NAME" < "$DROP_SCRIPT"
        echo "Database cleaned up."
    else
        echo "Cleanup script $DROP_SCRIPT not found!"
    fi
}

trap cleanup_on_error ERR

echo -n "Enter password for $DB_USER: "
read -s DB_PASS
echo
export MYSQL_PWD=$DB_PASS

echo "Initializing db schema: $DB_NAME"

for file in ../database/structure/*.sql; do
    echo "Running: $file"
    mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" "$DB_NAME" < "$file"
done

trap - ERR
unset MYSQL_PWD
echo "DB schema created successfully"