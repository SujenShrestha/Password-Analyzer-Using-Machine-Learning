import streamlit as st

#Machine Learning Package
import joblib

#Libraries to generate random password
import random
import string
import os


import requests
import hashlib
from PIL import Image
from check_pass import *

def gen_password(size):
    characters = string.difits = string.ascii_letters + string.punctuation
    generated_password = "".join(random.choice(characters) for x in range(size))
    return generated_password

def load_model(model_file):
    loaded_model = joblib.load(open(os.path.join(model_file),"rb"))
    return loaded_model

password_vectorizer = open("pswd_cv.pkl","rb")
pswd_cv = joblib.load(password_vectorizer)

def get_key(val,my_dict):
    for key,value in my_dict.items():
        if val == value:
            return key

password_labels = {"Weak":0,"Medium":1,"Strong":2}

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

            vect_password = pswd_cv.transform([password]).toarray()
            predictor = load_model("nv_pswd_model.pkl")
            prediction = predictor.predict(vect_password)

            result = get_key(prediction,password_labels)
            st.info(result)

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