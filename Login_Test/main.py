"""
Copyright (c) <2017> <Yicong Gong>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)

""" Uncomment the 1st for local testing and the 2nd one for deployment"""
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test101.db'        # Local testing
app.config.from_object(config)                                               # Deployment
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30), unique=False)
    goal = db.Column(db.String(120), unique=False)

    def __init__(self, name, email, password, goal):
        self.name = name
        self.email = email
        self.password = password
        self.goal = goal

    def __repr__(self):
        return '<User %r>' % self.name

@app.route('/')
@app.route('/welcome')
def front_page():
    return render_template('front_page.html')

@app.route('/login_post',methods=['GET', 'POST'])
def login_post():
    if request.method == 'POST':
        return perform_login()
    else:
        return "Invalid Request"

def perform_login():
    email = request.form.get("email")
    psw = request.form.get("password")
    users = User.query.all()
    found_user = User.query.filter_by(email=email).first()
    if found_user:  # User located
        if found_user.password == psw:
            return render_template('profile.html', name = found_user.name, email = found_user.email, \
            goal = found_user.goal)
        return "Password incorrect"
    else:
        return "No User found"

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up_page():
    return render_template('sign_up.html')

@app.route('/sign_up_post', methods=['GET', 'POST'])
def sign_up_post():
    if request.method == 'POST':
        return perform_sign_up()
    else:
        return "Invalid Request"

def perform_sign_up():
    name = request.form.get("name")
    email = request.form.get("email")
    psw = request.form.get("password")
    goal = request.form.get("goal")
    users = User.query.all()
    found_user = User.query.filter_by(email=email).first()
    if found_user==None:  # User located
        guest = User(name, email, psw, goal)
        db.session.add(guest)
        db.session.commit()
        found_user = guest
        return render_template('profile.html', name = found_user.name, email = found_user.email, \
            goal = found_user.goal)
    else:
        return "User Existed"

@app.route('/logout')
def logout():
    return redirect('/welcome')

@app.route('/init_all_this_is_a_secret_key_not_posting_here')
def init():
    from main import db
    db.create_all()
    return 'Set up'

if __name__ == '__main__':
    # app.debug = True
    app.run(host = '0.0.0.0', port = 5000)