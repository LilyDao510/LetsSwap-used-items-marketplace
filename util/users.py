# create a method to encode password and save to database
import bcrypt
def  encode_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')


# create a method to decode password and check if it matches the hashed password
def decode_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


# create a method to authenticate using google authenticate api
def authenticate_google(google_id_token):
    return True
    