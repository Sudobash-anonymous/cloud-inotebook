#!/bin/bash

TASK=$1

if [ -z "$TASK" ]; then
  echo "❌ Task ID required"
  exit 1
fi

pytest task/$TASK/task_tests.py 