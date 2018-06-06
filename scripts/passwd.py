import bcrypt

password = str.encode("123qweQWE", encoding="UTF-8")
password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
print(password_hash.decode("utf-8"))
