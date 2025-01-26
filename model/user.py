import bcrypt

class User:
    def __init__(self, username, password):
        self.username = username
        if isinstance(password, str):
            self.password = password.encode('utf-8')  # Store the plaintext password as bytes
            self.hash_password()  # Hash the password during initialization
        else:
            self.password = password  # For when we're working with an already hashed password

    def hash_password(self):
        """Hash the password using bcrypt and store the hashed password."""
        self.password = bcrypt.hashpw(self.password, bcrypt.gensalt())

    def check_password(self, password):
        """Check if the entered password matches the stored hashed password."""
        if isinstance(password, str):
            password = password.encode('utf-8')
        try:
            return bcrypt.checkpw(password, self.password)
        except Exception:
            return False