#!/bin/bash
echo "Iniciando backend..."
python3 -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000