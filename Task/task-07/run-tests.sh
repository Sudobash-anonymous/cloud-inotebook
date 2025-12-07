#!/bin/bash

TASK_ID=$1

if [ -z "$TASK_ID" ]; then
  echo "❌ Please provide a task id"
  echo "Usage: ./run-tests.sh task-07"
  exit 1
fi

echo "✅ Running tests for $TASK_ID ..."
pytest task/$TASK_ID/task_tests.py

if [ $? -eq 0 ]; then
  echo "✅ Tests passed for $TASK_ID"
else
  echo "❌ Tests failed for $TASK_ID"
  exit 1
fi