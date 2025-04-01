# Use the official Node.js image from the Docker Hub
FROM node:14-slim
FROM javascript-function
WORKDIR /app
COPY function/javascript/example_function.js .
CMD ["node", "example_function.js"]
