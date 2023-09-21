from models import Users


#method to verify email are unique
def verify_unique_user(email):
    user = Users.query.filter_by(email=email).first()
    if user:
        return False
    return True
