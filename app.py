from flask import Flask
from flask import Flask, render_template, url_for
from pymongo import MongoClient
app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/tax_form')
def tax_form():
    return render_template('tax_form.html')

@app.route('/term')
def term():
    return render_template('term.html')
