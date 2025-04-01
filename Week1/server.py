from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error

app = FastAPI()

# Database Connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="yash",
            database="serverless_db"
        )
        return conn
    except Error as e:
        print("Error connecting to MySQL:", e)
        return None

# Pydantic model for request body
class FunctionCreate(BaseModel):
    name: str
    route: str
    language: str
    timeout: int
    description: str

class FunctionUpdate(BaseModel):
    name: str = None
    route: str = None
    language: str = None
    timeout: int = None
    description: str = None

# CRUD Operations

# 1️⃣ Create a new function
@app.post("/functions/")
def create_function(func: FunctionCreate):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO functions (name, route, language, timeout, description) 
        VALUES (%s, %s, %s, %s, %s)
    """, (func.name, func.route, func.language, func.timeout, func.description))
    
    conn.commit()
    func_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return {"id": func_id, "message": "Function created successfully"}

# 2️⃣ Get function by ID
@app.get("/functions/{id}")
def get_function(id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM functions WHERE id = %s", (id,))
    function = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if function:
        return function
    raise HTTPException(status_code=404, detail="Function not found")

# 3️⃣ Get all functions
@app.get("/functions/")
def get_all_functions():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM functions")
    functions = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return {"functions": functions}

# 4️⃣ Update function metadata
@app.put("/functions/{id}")
def update_function(id: int, func: FunctionUpdate):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    cursor = conn.cursor()
    
    # Dynamic update query
    update_fields = []
    values = []
    for field, value in func.dict(exclude_unset=True).items():
        update_fields.append(f"{field} = %s")
        values.append(value)
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    values.append(id)
    query = f"UPDATE functions SET {', '.join(update_fields)} WHERE id = %s"
    cursor.execute(query, values)
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return {"message": "Function updated successfully"}

# 5️⃣ Delete function
@app.delete("/functions/{id}")
def delete_function(id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM functions WHERE id = %s", (id,))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return {"message": "Function deleted successfully"}

if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        print("✅ Successfully connected to the database!")
        conn.close()
    else:
        print("❌ Failed to connect to the database!")