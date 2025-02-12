import streamlit as st
import json
import os

# Define the path for the JSON file
FILE_PATH = "users.json"

# Function to load users from JSON file
def load_users():
    if not os.path.exists(FILE_PATH):
        return {"users": []}  # Return empty structure if file doesn't exist
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {"users": []}  # Handle broken JSON files

# Function to save users to JSON file
def save_users(users):
    with open(FILE_PATH, "w") as file:
        json.dump(users, file, indent=4)

# Function to check if a user exists
def user_exists(username):
    return any(user["username"] == username for user in load_users()["users"])

# Function to add a new user
def add_user(username, password):
    data = load_users()
    if user_exists(username):
        return False  # User already exists
    data["users"].append({"username": username, "password": password})
    save_users(data)
    return True  # Successfully added

# Streamlit UI
st.title("User Signup")

new_username = st.text_input("Username")
new_password = st.text_input("Password", type="password")

if st.button("Sign Up"):
    if user_exists(new_username):
        st.error("Username already exists. Please choose another one.")
    else:
        add_user(new_username, new_password)
        st.success("Signup successful! You can now log in.")

