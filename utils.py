import hashlib
import re

def hash_password(password):

    #Hashes a password using SHA-256 algorithm.
    
    return hashlib.sha256(password.encode()).hexdigest()

def validate_username(username):
    """
    Validates a username.
    Requirements:
    - Username must be between 4 and 20 characters long.
    - Only alphanumeric characters and underscores are allowed.
    """
    if not re.match("^[a-zA-Z0-9_]{4,20}$", username):
        return False
    return True

def validate_password(password):
    """
    Validates a password.
    Requirements:
    - Password must be at least 8 characters long.
    - Password must contain at least one uppercase letter, one lowercase letter, and one digit.
    """
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    return True
