from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "42519h",
    "database": "assignment_login"
}

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM customer_profile WHERE c_name = %s AND c_password = %s", (username, password))
    result = cursor.fetchone()

    if result:
        return f'User Authorized. Your IP Address: {request.remote_addr}'
    else:
        return 'Unauthorized User'

@app.route('/forgot_password')
def forgot_password_page():
    return render_template('forgot_password.html')

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    
    username = request.form['username']
    mobile = request.form['mobile']

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM customer_profile WHERE c_name = %s AND c_mobile = %s", (username, mobile,))
    result = cursor.fetchone()

    if result:
        # Send password recovery instructions to the user
        return 'Password recovery instructions sent to your registered mobile number.'
    else:
        return 'Mobile number not found in our records.'

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    new_username = request.form['new-username']
    new_password = request.form['new-password']
    new_mobile = str(request.form['new-mobile'])

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("INSERT INTO customer_profile (c_name, c_password, c_mobile) VALUES (%s, %s, %s)", (new_username, new_password, new_mobile))
    connection.commit()

    return 'Account created successfully.'

if __name__ == '__main__':
    app.run()
