#!/bin/sh
if [ -f "/function/package.json" ]; then
    npm install --production
fi
exec node /function/handler.js