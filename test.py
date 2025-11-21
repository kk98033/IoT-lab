from flask import Flask, session, request, redirect

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/login', methods=['POST'])
def login():
    session['user'] = request.form['username']
    return redirect('/home')

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/login')
    return "Welcome, " + session['user']

