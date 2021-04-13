from flask import Flask, render_template, url_for, request, redirect

from pymongo import MongoClient
client = MongoClient(
    'mongodb+srv://test:test@cluster0.fcu7b.mongodb.net/test?retryWrites=true&w=majority')
db = client.taxmanager
accounts = db.accounts

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
    

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/check_login', methods=['GET', 'POST'])
def check_login():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['psw']
    for i in accounts.find():
        if i.key() == username and i.value() == password:
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
        password_repeat=request.form['psw-repeat']
        if password == password_repeat:
            credentials={
                "email":email,
                "password":password
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


# test to insert data to the data base
@app.route("/test")
def test():
    accounts.insert_one({"name": "John"})
    return "Connected to the data base!"

