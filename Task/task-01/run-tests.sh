#!/bin/bash

# Usage: ./run-tests.sh task-01

TASK=$1

if [ -z "$TASK" ]; then
  echo "❌ No task ID provided."
  echo "✅ Usage: ./run-tests.sh task-01"
  exit 1
fi

TEST_PATH="tasks/$TASK/task_tests.py"

if [ ! -f "$TEST_PATH" ]; then
  echo "❌ Test file not found at: $TEST_PATH"
  exit 1
fi

echo "✅ Running tests for $TASK ..."
pytest "$TEST_PATH"