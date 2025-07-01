import re
import secrets
import hashlib
from db import get_connection

def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(32)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return password_hash, salt

def is_valid_egyptian_phone(phone):
        return re.match(r'^01[0125][0-9]{8}$', phone) is not None

def is_valid_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

def register(cur,conn):
    print("=== User Registration ===")
    
    while True:
        first_name = input("First name: ").strip()
        if first_name:
            break
        print("First name cannot be empty.")

    while True:
        last_name = input("Last name: ").strip()
        if last_name:
            break
        print("Last name cannot be empty.")

    while True:
        email = input("Email: ").strip()
        if not email:
            print("Email cannot be empty.")
        elif not is_valid_email(email):
            print("Invalid email format.")
        else:
            break
        
    while True:
        password = input("Password: ").strip()
        if not password:
            print("Password cannot be empty.")
            continue
        elif len(password) < 8:
            print("Password must be at least 8 characters long.")
            continue

        confirm_password = input("Confirm Password: ").strip()
        if password != confirm_password:
            print("Passwords do not match.")
            continue
        break

    while True:
        mobile_phone = input("Mobile number (Egyptian format): ").strip()
        if not mobile_phone:
            print("Mobile number cannot be empty.")
        elif not is_valid_egyptian_phone(mobile_phone):
            print("Invalid Egyptian mobile number.")
        else:
            break
    
    password_hash,salt = hash_password(password)

    try:
        with get_connection() as (conn, cur):
            create_table_query = '''
                    CREATE TABLE IF NOT EXISTS users(
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    email VARCHAR(50) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    mobile_phone VARCHAR(50),
                    salt TEXT NOT NULL
                    )
                '''
            cur.execute(create_table_query)

            insert_query = '''
            INSERT INTO users (first_name,last_name,email,password,mobile_phone,salt) 
            VALUES (%s,%s,%s,%s,%s,%s)
            '''

            cur.execute(insert_query, (first_name,last_name,email,password_hash,mobile_phone,salt))

            conn.commit()
            print("Registration successful, you can now login!")
    except Exception as error:
        print(f"Database connection failed: {error}")

def login():
    print("=== User Login ===")
    while True:
        email = input("Email: ").strip()
        if not email:
            print("Email cannot be empty.")
        elif not is_valid_email(email):
            print("Invalid email format.")
        else:
            break

    while True:
        password = input("Password: ").strip()
        if not password:
            print("Password cannot be empty.")
            continue
        break


    try:
        with get_connection() as (conn, cur):

            cur.execute("SELECT user_id, password,salt FROM users WHERE email = %s", (email,))
            result = cur.fetchone()
            
            if not result:
                print("No user found")  
                return False
            
            user_id,stored_hash, stored_salt = result
            entered_hash, _ = hash_password(password, stored_salt) 
            
            if entered_hash == stored_hash:
                print("Login successful")
                return user_id
            else:
                print("Invalid credentials") 
                return False
    except Exception as error:
        print(f"Database connection failed: {error}")