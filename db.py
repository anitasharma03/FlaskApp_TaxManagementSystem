from flask import Flask
from pymongo import MongoClient
client = MongoClient(
    'mongodb+srv://KaranGaba:<KaranGaba>@cluster0.fcu7b.mongodb.net/tax_manager?retryWrites=true&w=majority')
db = client.taxmanager
accounts = db.accounts