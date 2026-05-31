#!/bin/bash
mkdir -p /shared_data
python run_trader.py &
uvicorn main:app --host 0.0.0.0 --port 8080