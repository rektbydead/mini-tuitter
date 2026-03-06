from passlib.hash import argon2

class HashingContext:

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return argon2.verify(plain_password, hashed_password)

    @staticmethod
    def generate_hash(plain_password):
        return argon2.hash(plain_password)
