
        FROM serverless-python
        WORKDIR /app
        COPY example_function.python .
        CMD ["python3", "example_function.py"] if lang == "python" else CMD ["node", "example_function.js"]
        