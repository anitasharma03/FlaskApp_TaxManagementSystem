from flask import Flask, render_template, flash, url_for, request, redirect, session
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from flask_login import LoginManager, login_user, current_user
import datetime

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
    filed_taxes = user_info.find()
    username = session["username"]
    return render_template('home.html', filed_taxes=filed_taxes, username=username)

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
        return render_template('register.html')


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


def calc_tax(losses, rrsp, yearly_income, additional_income, yearly_expense):
    loss_percentage = (int(losses) / 100) * 1.2
    rrsp_percent = (int(rrsp)/100)*2.5
    total_income = int(yearly_income) + \
        int(additional_income) + int(yearly_expense)
    tax = (total_income/100) * 15
    total_tax = loss_percentage + rrsp_percent + tax
    return total_tax


@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        fname = request.form['firstname']
        lname = request.form['lastname']
        email = request.form['email']
        phone = request.form['Phone']
        address = request.form['address']
        address2 = request.form['address2']
        sex = request.form['sex']
        sin = request.form['sin']
        netincome = request.form['NetIncome']
        extraincome = request.form['ExtraIncome']
        expenses = request.form['expenses']
        losses = request.form['losses']
        rrsp = request.form['rrsp']
        filed_on = datetime.datetime.now()
        details = {
            "firstname": fname,
            "lastname": lname,
            "email": email,
            "phone": phone,
            "address": address,
            "address2": address2,
            "sex": sex,
            "sin": sin,
            "netincome": netincome,
            "extraincome": extraincome,
            "expenses": expenses,
            "losses": losses,
            "rrsp": rrsp,
            "filed_on": filed_on,
            "total_tax": calc_tax(losses, rrsp, netincome, extraincome, expenses)
        }
        user_info.insert_one(details)
        flash('Your Details has been submitted')
        return redirect("/detail")
    return redirect("/home")


@app.route('/profile')
def profile():
    if session['username']:
        return render_template('profile.html')
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
        return flash('User has been updated')
    return redirect("/update_profile")


@app.route('/detail')
def detail():
    filed_taxes = user_info.find()
    username = session["username"]
    return render_template('showTaxDetail.html', filed_taxes=filed_taxes, username=username)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('logout.html')
