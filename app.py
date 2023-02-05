import streamlit as st

#Libraries to generate random password
import random
import string

import numpy as np
import pickle
from check_pass import *

def gen_password(size):
    characters = string.digits + string.ascii_letters + string.punctuation
    generated_password = "".join(random.choice(characters) for x in range(size))
    return generated_password

def word_to_char(word):
    return list(word)

def load_vectorizer():
    #Loading vectorizer from pickle file
    file = open("tfidf_password_strength.pickle",'rb')
    saved_vectorizer = pickle.load(file)
    file.close()
    return saved_vectorizer
def load_model():
    #Loading model from pickle file
    file = open("final_model.pickle",'rb')
    final_model = pickle.load(file)
    file.close()
    return final_model

def password_strength_check(input,vectorizer,model):
    X_password=np.array([input])
    X_predict=vectorizer.transform(X_password)
    y_pred=model.predict(X_predict)
    strengh=y_pred[0]
    if strengh==0:
        return 'Weak Password'
    if strengh==1:
        return 'Medium Password'
    if strengh==2:
        return 'Strong Password'

def api(pwned):
	count = api_check(pwned)
	if count:
		st.markdown(f"<font color=‘ff0000’ size=5>Oh no! Your password has been seen {count} times before.</font>", unsafe_allow_html=True)
		st.markdown(f"<font color=‘ff0000’ size=3>This password has previously appeared in a data breach and should never be used. If you've ever used it anywhere before, change it!</font>", unsafe_allow_html=True)
	else:
		st.markdown(f'<font color=‘089e00’ size=5>Your password is secure</font>', unsafe_allow_html=True)
		st.markdown(f"<font color=‘089e00’ size=3>This password wasn't found in any of the compromised Passwords loaded into Have I Been Pwned Database.</font>", unsafe_allow_html=True)
	return 

def main():
    """Password Analyzer"""
    st.title("Password Strength Analyzer")
    #st.subheader("Final Year Project")

    activities = ["Check Password Strength","Password Generator"]
    choice = st.sidebar.selectbox("Select Activity",activities)

    if choice == "Check Password Strength":
        st.subheader("Test Your Password Strength")
        password = st.text_input("Enter Password",type="password")
        if st.button("Check"):
            vectorizer=load_vectorizer()
            model=load_model()
            st.write(password_strength_check(password,vectorizer,model))

            api(password)

    elif choice == "Password Generator":
        st.subheader("Generate Random Password")
        number = st.number_input("Enter the length of password.",8,25)
        st.write(number)
        if st.button("Generate"):
            custom_password = gen_password(number)
            st.write(custom_password)
        
if __name__ == '__main__':
    main()