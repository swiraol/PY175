import bcrypt

passwords = ['secret', 'password123', 'test123', 'user123']

for password in passwords:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    print(f"Plain: {password}, Hashed: {hashed_password.decode('utf-8')}")