#!/bin/bash

# Usage: ./tasks/task-05/run-tests.sh task-05

TASK_ID=${1:-task-05}

TEST_PATH="tasks/$TASK_ID/task_tests.py"

if [ ! -f "$TEST_PATH" ]; then
  echo "❌ Test file not found at: $TEST_PATH"
  exit 1
fi

echo "✅ Running tests for $TASK_ID ..."
pytest "$TEST_PATH"