import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt() 
    hashed_password = bcrypt.hashpw(password.encode(), salt) 
    return hashed_password.decode() 

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


# # Example Usage
# password = "mypassword123"
# hashed_pw = hash_password(password)
# print("Hashed Password:", hashed_pw)  
