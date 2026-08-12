import jwt
usr = {'admin':True}
print(jwt.encode(usr, "secret", algorithm="HS256"))

