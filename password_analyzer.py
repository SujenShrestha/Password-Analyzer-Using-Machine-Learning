import numpy as np
import pickle

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
    return y_pred[0]