#!/bin/bash -e

function wait_for_container_logs()
{
  local container_name=$1
  local message=$2
  local max_attempts=180
  local success=0

  echo
  echo -n "Waiting for ${container_name} logs to contain the message: ${message}"
  for (( try=0; try < max_attempts; ++try )); do
    if docker logs "${container_name}" 2>&1 | grep -q "${message}"; then
      success=1
      break
    fi
    echo -n "."
    sleep 2
  done

  if (( success )); then
    echo ""
  else
    echo "${container_name} not started as expected"
    docker logs ${container_name}
    exit 1
  fi
}

function run_oracle_backups()
{
  local log_message="Finished importing Beacon backups"
  echo "Standing up Oracle DB backups"
  docker-compose pull -q oracle-db
  docker-compose up -d oracle-db

  wait_for_container_logs "oracle-db" "${log_message}"
}

function run_migration()
{
  echo "Attempting to run the migration"
  docker-compose up etl
}

run_oracle_backups
run_migration