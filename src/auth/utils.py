from passlib.context import CryptContext

password_context=CryptContext(
    schemas=['bcrypt']

)

def generate_password_hash(password:str):
    hash=password_context.hash(password)

    return hash

def verify_passsword(password:str,hash_password:str):
    return password_context.verify(password,hash_password)