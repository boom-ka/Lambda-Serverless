
        FROM serverless-javascript
        WORKDIR /app
        COPY example_function.js .
        CMD ["python3", "example_function.py"] if lang == "python" else CMD ["node", "example_function.js"]
        