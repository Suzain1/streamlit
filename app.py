import json
import streamlit as st
import os

USER_FILE = "users.json"

# Function to load users from JSON
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            try:
                return json.load(file)  # Load the JSON file
            except json.JSONDecodeError:
                return []  # Return empty list if JSON is invalid
    return []

# Function to save users to JSON
def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)  # Save users with formatting

# Function to check if user exists
def user_exists(username):
    users = load_users()
    return any(user["username"] == username for user in users)

# Function to authenticate user login
def authenticate(username, password):
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return True
    return False

# Streamlit UI
st.title("User Authentication")

# Tabs for Signup and Signin
option = st.radio("Choose an option:", ["Sign Up", "Sign In"])

if option == "Sign Up":
    st.subheader("Create an Account")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if user_exists(new_username):
            st.error("Username already exists. Please choose another one.")
        else:
            users = load_users()
            users.append({"username": new_username, "password": new_password})
            save_users(users)
            st.success("Signup successful! You can now log in.")

elif option == "Sign In":
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or password.")

