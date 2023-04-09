import streamlit as st
import random
import string
import numpy as np
import pickle
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

# Generate a random password of given length
def generate_password(length):
    # Combine digits, letters, and punctuation as possible characters for the password
    characters = string.digits + string.ascii_letters + string.punctuation
    # Randomly select characters and join them to form the password
    generated_password = "".join(random.choice(characters) for _ in range(length))
    return generated_password

# Convert a given word (string) to a list of individual characters
def word_to_char(word):
    return list(word)

# Display password compliance guidelines based on NIST recommendations
def display_password_compliance():
    st.write("\n")
    st.subheader("NIST Password Guidelines")
    filename = "NIST.txt"
    with open(filename, "r") as file:
        i = 1
        for line in file:
            line = line.strip()
            if line:
                st.write(f"{i}. {line}")
                i += 1

# Load the pre-trained vectorizer from a pickle file
def load_vectorizer():
    with open("tfidf_password_strength.pickle", 'rb') as file:
        saved_vectorizer = pickle.load(file)
    return saved_vectorizer

# Load the pre-trained model from a pickle file
def load_model():
    with open("final_model.pickle", 'rb') as file:
        final_model = pickle.load(file)
    return final_model

# Check and display the strength of the input password
def check_password_strength(password_input, vectorizer, model):
    X_password = np.array([password_input])
    # Transform the input password using the pre-trained vectorizer
    X_predict = vectorizer.transform(X_password)
    # Make predictions using the pre-trained model
    y_pred = model.predict(X_predict)
    strength = y_pred[0]
    st.write('\n\n')
    # Display the password strength based on the predicted strength value
    if strength == 0:
        return st.error('**Your Password is Weak.** \n\n **A strong password consists of a combination of letters, numbers and symbols.** \n\n **An example of a strong password would be P@$sw0rd&1.** \n\n **In the example, the password consists of a combination of different characters which makes it difficult to be guessed or cracked by hackers.**')
    if strength == 1:
        return st.warning('**Your Password is Average.** \n\n **A strong password consists of a combination of letters, numbers and symbols.** \n\n **An example of a strong password would be P@$sw0rd&1.** \n\n **In the example, the password consists of a combination of different characters which makes it difficult to be guessed or cracked by hackers.**')
    if strength == 2:
        return st.success('**Your Password is Strong.**')

# Display API result
def display_api_result(compromised_count):
    # Check if the password has been compromised before and display an appropriate message
    if compromised_count:
        st.markdown(f"<font color=‘ff0000’ size=5>Oh no! Your password has been seen {compromised_count} times before.</font>", unsafe_allow_html=True)
        st.markdown(f"<font color=‘ff0000’ size=3>This password has previously appeared in a data breach and should never be used. If you've ever used it anywhere before, change it!</font>", unsafe_allow_html=True)
    else:
        st.markdown(f'<font color=‘089e00’ size=5>Your password is secure</font>', unsafe_allow_html=True)
        st.markdown(f"<font color=‘089e00’ size=3>This password wasn't found in any of the compromised Passwords loaded into Have I Been Pwned Database.</font>", unsafe_allow_html=True)

def main():
    # Define the available activities in the application
    activities = ["Password Analyzer", "Password Generator"]
    
    # Create a sidebar selection box for the user to choose an activity
    choice = st.sidebar.selectbox("Select Activity", activities)
    
    # If the user chooses "Password Analyzer" activity
    if choice == "Password Analyzer":
        st.title("Password Strength Analyzer")
        st.subheader("Test Your Password Strength")
        
        # Get the user's input for the password
        password = st.text_input("Enter Password", type="password")
        st.write("\n\n")
        
        # When the user clicks the "Check" button
        if st.button("Check"):
            # Load the vectorizer and model
            vectorizer = load_vectorizer()
            model = load_model()
            
            # Check and display the password strength
            check_password_strength(password, vectorizer, model)
            
            # Check the password against the API and display the result
            compromised_count = check_password_api(password)
            display_api_result(compromised_count)
        
        # Display the password compliance guidelines
        display_password_compliance()

    # If the user chooses "Password Generator" activity
    elif choice == "Password Generator":
        st.subheader("Generate Random Password")
        
        # Get the user's input for the password length
        password_length = st.number_input("Enter the length of password.", 10, 64)
        st.write(password_length)
        
        # When the user clicks the "Generate" button
        if st.button("Generate"):
            # Generate a random password based on the user's input
            custom_password = generate_password(password_length)
            
            # Display the generated password
            st.write(custom_password)

# Execute the main function
if __name__ == '__main__':
    main()