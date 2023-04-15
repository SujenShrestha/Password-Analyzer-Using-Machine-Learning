import streamlit as st
from password_analyzer import check_password_strength, load_vectorizer, load_model
from api_check import check_password_api
from nist_compliance import display_password_compliance
from password_generator import generate_password

# Convert a given word (string) to a list of individual characters
def word_to_char(word):
    return list(word)

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
            strength = check_password_strength(password, vectorizer, model)
            if strength == 0:
                st.error("**Your Password is Weak.** \n\n **A strong password consists of a combination of letters, numbers and symbols.** \n\n **An example of a strong password would be P@$sw0rd&1.** \n\n **In the example, the password consists of a combination of different characters which makes it difficult to be guessed or cracked by hackers.**")
            elif strength == 1:
                st.warning("**Your Password is Average.** \n\n **A strong password consists of a combination of letters, numbers and symbols.** \n\n **An example of a strong password would be P@$sw0rd&1.** \n\n **In the example, the password consists of a combination of different characters which makes it difficult to be guessed or cracked by hackers.**")
            elif strength == 2:
                st.success("**Your Password is Strong.**")

            # Check the password against the API and display the result
            compromised_count = check_password_api(password)
            if compromised_count:
                st.error(f"**Your password has been compromised {compromised_count} times before.**")
            else:
                st.success("**Your password was not seen in compromised password database of Have I Been Pwned.**")

        # Display the password compliance guidelines
        guidelines = display_password_compliance()
        st.subheader("NIST Password Guidelines:")
        for i, guideline in enumerate(guidelines, start=1):
            st.write(f"{i}. {guideline}")

    # If the user chooses "Password Generator" activity
    elif choice == "Password Generator":
        st.subheader("Generate Random Password")

        # Get the user's input for the password length
        password_length = st.number_input("Enter the length of password.", 10, 64)
        st.write("Password Length: ", password_length)

        # When the user clicks the "Generate" button
        if st.button("Generate"):
            # Generate a random password based on the user's input
            custom_password = generate_password(password_length)

            # Display the generated password
            st.write(custom_password)

# Execute the main function
if __name__ == '__main__':
    main()