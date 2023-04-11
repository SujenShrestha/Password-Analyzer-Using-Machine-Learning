import requests
import hashlib

API_URL = 'https://api.pwnedpasswords.com/range/'

# Request data from the API
def request_api_data(query_char):
    url = API_URL + query_char
    response = requests.get(url)

    # Raise an error if the API request is unsuccessful
    if response.status_code != 200:
        raise RuntimeError(f'ERROR FETCHING: {response.status_code}, CHECK API AND TRY AGAIN')
    return response

# Get the count of compromised passwords
def get_compromised_count(hashes, tail_hash):
    # Split the response text into lines and then into hash and count pairs
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for hash, count in hashes:
        if hash == tail_hash:
            return count
    return 0

# Check if the password has been compromised using the API
def check_password_api(password):
    # Calculate the SHA-1 hash of the password
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_chars, tail = sha1_password[:5], sha1_password[5:]
    response = request_api_data(first5_chars)
    return get_compromised_count(response, tail)