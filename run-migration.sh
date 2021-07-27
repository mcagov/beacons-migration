#!/bin/bash -e

function wait_for_container_logs
{
  local container_name=$1
  local message=$2

  while ! docker logs "${container_name}" | grep -q "${message}";
  do
    sleep 1
    echo "Waiting for ${container_name} logs to contain the message: ${message}"
  done
}

function run_oracle_backups
{
  local log_message="Finished importing Beacon backups"
  echo "Standing up Oracle DB backups"
  docker-compose up -d oracle-db

  echo "Waiting for Oracle DB logs to container the message ${log_message}"
  wait_for_container_logs "oracle-db" "${log_message}"
}

function run_migration
{
  echo "Attempting to run migration"
  docker-compose up etl
}

run_oracle_backups
run_migration