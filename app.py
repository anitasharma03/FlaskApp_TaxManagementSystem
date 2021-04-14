from flask import Flask, render_template, url_for, request, redirect
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from flask_login import LoginManager, login_user, current_user
client = MongoClient(
    'mongodb+srv://test:test@cluster0.fcu7b.mongodb.net/test?retryWrites=true&w=majority')
db = client.taxmanager
accounts = db.accounts

app = Flask(__name__)

bcrypt = Bcrypt()


@app.route('/')
@app.route('/landing')
def landing_page():
    return render_template('landing_page.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/check_login', methods=['GET', 'POST'])
def check_login():
    if request.method == 'POST':
        username = user.query.get(form.username.data)
        password = request.form['psw']
    for i in accounts.find():
        if i["email"] == username and bcrypt.check_password_hash(i["password"], password):
            login_user(username)
            return redirect("/home")
        else:
            continue
    return redirect("/login")


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/make_account', methods=['GET', 'POST'])
def make_account():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['psw']
        password_repeat = request.form['psw-repeat']
        if password == password_repeat:
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            credentials = {
                "email": email,
                "password": password
            }
            accounts.insert_one(credentials)
            return redirect("/home")
        return redirect("/register")


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


@app.route('/contactus')
def contactus():
    return render_template('contactus.html')


@app.route('/term')
def term():
    return render_template('term.html')


@app.route('/form')
def form():
    return render_template('tax_form.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')
