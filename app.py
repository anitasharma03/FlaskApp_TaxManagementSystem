from flask import Flask, render_template, flash, url_for, request, redirect, session
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from flask_login import LoginManager, login_user, current_user
from bson.objectid import ObjectId

client = MongoClient(
    'mongodb+srv://test:test@cluster0.fcu7b.mongodb.net/test?retryWrites=true&w=majority&authMechanism=SCRAM-SHA-1&ssl=true&ssl_cert_reqs=CERT_NONE')
db = client.taxmanager
accounts = db.accounts
user_info = db.formDetails

app = Flask(__name__)
app.secret_key = 'secret_key'

bcrypt = Bcrypt()


@app.route('/')
@app.route('/landing')
def landing():
    return render_template('landing_page.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    if 'username' not in session:
        return render_template('landing_page.html')
    else:
        return render_template('home.html')


@app.route('/check_login', methods=['GET', 'POST'])
def check_login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['psw']
    for i in accounts.find():
        if i["email"] == username and bcrypt.check_password_hash(i["password"], password):
            session['username'] = username
            flash('You were successfully logged in')
            return redirect("/home")
        else:
            continue
    flash('Wrong username or password. Please retry')
    return redirect("/landing")


@app.route('/register')
def register():
    if 'username' not in session:
        return render_template('register.html')
    else:
        return render_template('home.html')


@app.route('/make_account', methods=['GET', 'POST'])
def make_account():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['psw']
        password_repeat = request.form['psw-repeat']
        if password == password_repeat:
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            session["username"] = email
            credentials = {
                "email": email,
                "password": password
            }
            accounts.insert_one(credentials)
            session["username"] = email
            flash('User has been registered. You can Login now')
            return redirect("/landing")
        else:
            flash('Passwords do not match. Please retry')
            return redirect("/register")
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
    if 'username' in session:
        return render_template('tax_form.html')
    else:
        return redirect("/landing")


@app.route('/profile')
def profile():
    if session['username']:
        username = session["username"]
        for i in user_info.find():
            if i["email"] == username:
                detail = {
                    "firstname": i["firstname"],
                    "lastname": i["lastname"],
                    "email": i["email"],
                    "phone": i["phone"],
                    "address": i["address"]
                }
        return render_template('profile.html', accounts=user_info, detail=detail)
    else:
        return redirect("/landing")


@app.route('/update_profile', methods=['POST'])
def update_profile():
    if request.method == 'POST':
        data = {
            "firstName": request.form['savedFname'],
            "lastName": request.form['savedLname'],
            "email": request.form['savedEmail'],
            "number": request.form['savedNumber'],
            "address": request.form['savedAddress'],
        }
        # TODO: update database
        # profile.insert_one(data)
        return flash('User has been updated')
    return redirect("/update_profile")


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('logout.html')
