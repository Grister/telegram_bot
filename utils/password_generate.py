import random


def escape_password(password: str) -> str:
    special_chars = "\\`*_{}[]()#+-.!"
    return ''.join(f'\\{char}' if char in special_chars else char for char in password)


def generate_password(length):
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    lowercase_chars = 'abcdefghijklnopqrstuvwxyz'
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

    # Shuffle the list to mix the required characters with the random ones
    random.shuffle(password)

    return ''.join(password)
