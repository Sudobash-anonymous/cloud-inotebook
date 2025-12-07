#!/bin/bash

TASK=$1

if [ -z "$TASK" ]; then
  echo "❌ Task ID required. Example:"
  echo "./run-tests.sh task-01"
  exit 1
fi

echo "✅ Running tests for $TASK"
pytest task/$TASK/task_tests.py 