from flask import Flask, render_template, request, redirect, url_for
import random
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Ensure users.txt exists
if not os.path.exists('users.txt'):
    open('users.txt', 'w').close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        gmail = request.form['gmail']
        phone = request.form['phone']
        address = request.form['address']
        
        app_id = f"APP{random.randint(1000, 9999)}"  # Generate a simple App ID

        with open('users.txt', 'a') as f:
            f.write(f"{name},{gmail},{phone},{address},{app_id}\n")

        return render_template('signup_success.html', app_id=app_id)

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        app_id = request.form['app_id']
        
        with open('users.txt', 'r') as f:
            users = f.readlines()
            for user in users:
                user_details = user.strip().split(',')
                if app_id in user_details:
                    # Redirect to home upon successful login with user details
                    return render_template('startuppage.html', app_id=user_details[4], name=user_details[0], email=user_details[1], phone=user_details[2], address=user_details[3])

        return "Login Failed. Invalid App ID."

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)