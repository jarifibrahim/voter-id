from flask import Flask, render_template, request, flash, redirect, jsonify
from mongoengine import *
import random
import os

app = Flask(__name__)

connect_string = os.environ['MONGODB_CONNECT_STRING']
db_name = os.environ['db']
secret_key = os.environ['secret']

connect(host=connect_string)
app.config['MONGODB_DB'] = db_name
app.config['SECRET_KEY'] = secret_key

class Users(Document):
    name = StringField(unique=True)
    date = StringField()
    aadhar_number = IntField()
    voter_id = IntField(unique=True)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        form = request.json
        user = Users()
        user.name = request.form['name']
        user.aadhar_number = request.form['aadhar']
        user.date = request.form['bday']
        user.voter_id = random.randint(1000, 20000)
        try:
            user.save()
        except Exception as e:
            z = e
            print z
            flash("User already exists", 'text-danger')
            return redirect('/')
        flash("User successfully registered", 'text-success')
    return redirect("/result")


@app.route("/result", methods=['GET', 'POST'])
def result():
    user = Users.objects()
    return render_template("result.html", result=user)

if __name__ == '__main__':
    app.run(debug=True)
