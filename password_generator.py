import random
import string

# Generate a random password of given length
def generate_password(length):
    # Combine digits, letters, and punctuation as possible characters for the password
    characters = string.digits + string.ascii_letters + string.punctuation
    # Randomly select characters and join them to form the password
    generated_password = "".join(random.choice(characters) for _ in range(length))
    return generated_password