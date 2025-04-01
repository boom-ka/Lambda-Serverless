import time

def handler():
    time.sleep(5)  # Simulate a long-running function (5 seconds)
    return {"message": "Hello from Python!"}

if __name__ == "__main__":
    print(handler())  # Call the function and print output
