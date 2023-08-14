#!/bin/bash

docker compose build
echo "\n\nCreating docker volumes\n"

docker volume create osprey-postgres-data
docker volume create osprey-endpoint-data
docker volume create osprey-proxystore-data

echo "\n\nSetting up Globus Compute Endpoint"

echo "\nThe Globus Endpoint UUID is : "
docker compose run -it globus-endpoint globus-compute-endpoint start default

echo "\nThe Globus Flow Functions UUIDs are : "
docker compose run -it globus-endpoint python /app/osprey/worker/lib/globus_flow_helper.py

echo "\n\nRunning migrations"
docker compose exec -it postgres-database psql -U postgres -c 'create database osprey_development;'
docker compose run -it web flask db upgrade

echo "\n\nSetting up Globus Flow Worker"
docker compose exec -it web python /app/osprey/server/jobs/timer.py

echo "\n\nGo to docker-compose.yml and replace

- GLOBUS_WORKER_UUID= <globus-endpoint-uuid>
- GLOBUS_FLOW_DOWNLOAD_FUNCTION= <download-uuid>
- GLOBUS_FLOW_COMMIT_FUNCTION= <commit-uuid>

"