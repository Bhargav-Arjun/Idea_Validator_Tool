#!/bin/bash

echo "🔧 Starting idea-validator backend..."
python3 -m app.utils.rate_limiter # init DB
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
