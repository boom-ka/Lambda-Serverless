#!/bin/sh
if [ -f "/function/requirements.txt" ]; then
    pip install --no-cache-dir -r /function/requirements.txt
fi
exec python /function/handler.py