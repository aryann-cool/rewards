import os
import re
import json
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

USERS_FILE = 'users.json'

def load_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not email or not password or not confirm_password:
            return render_template('signup.html', error="All fields are required.")
        if len(username) < 6:
            return render_template('signup.html', error="Username must be at least 6 characters long.")
        if len(password) < 8:
            return render_template('signup.html', error="Password must be at least 8 characters long.")
        if password != confirm_password:
            return render_template('signup.html', error="Passwords do not match.")
        if not is_valid_email(email):
            return render_template('signup.html', error="Invalid email address.")

        users = load_users()
        for user in users:
            if user['username'] == username or user['email'] == email:
                return render_template('signup.html', error="Username or email already exists.")

        # Save the user directly without verification
        users.append({"username": username, "email": email, "password": password})
        save_users(users)

        return redirect('/login')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('login.html', error="All fields are required.")

        users = load_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                return redirect('/')

        return render_template('login.html', error="Invalid username or password.")

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
