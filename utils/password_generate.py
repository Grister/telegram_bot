import random


def generate_password(length):
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    uppercase_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digit_chars = '1234567890'

    # Ensure at least one uppercase letter and one digit
    password = [
        random.choice(uppercase_chars),
        random.choice(digit_chars)
    ]

    # Fill the rest of the password length with random characters
    for i in range(length - 2):
        password.append(random.choice(chars))

    random.shuffle(password)

    return ''.join(password)
