#!/bin/bash
mongosh -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" --authenticationDatabase admin <<EOF
use pontos_turisticos_db
if (!db.getCollectionNames().includes('locais')) {
  db.createCollection('locais')
}
EOF

mongoimport --db pontos_turisticos_db --collection locais --file /docker-entrypoint-initdb.d/pontos_turisticos.json --jsonArray -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" --authenticationDatabase admin
