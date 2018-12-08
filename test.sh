#!/bin/sh
PROJECT_DIR=${0%/*}
PYTHONPATH=${PROJECT_DIR}:${PYTHONPATH} python "${PROJECT_DIR}"/test.py
