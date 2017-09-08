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
from helper import *
import MySQLdb
import config
import json

app = Flask(__name__)

""" Uncomment the 1st for local testing and the 2nd one for deployment"""
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test101.db'        # Local testing
# app.config.from_object(config)                                               # Deployment
db = config.connect_to_cloudsql()
c = db.cursor()
c.execute("""USE Web_Dev""")

""" The following is for event handlers"""
@app.route('/')
@app.route('/welcome')
def front_page():
    return render_template('front_page.html')

@app.route('/login_post',methods=['GET', 'POST'])
def login_post():
    if request.method == 'POST':
        return perform_login(request, c)
    else:
        return "Invalid Request"

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up_page():
    return render_template('sign_up.html')

@app.route('/sign_up_post', methods=['GET', 'POST'])
def sign_up_post():
    if request.method == 'POST':
        return perform_sign_up(request, c)
    else:
        return "Invalid Request"

@app.route('/logout')
def logout():
    return redirect('/welcome')

@app.route('/init_all_this_is_a_secret_key_not_posting_here')
def init():

    c.execute("""DROP TABLE User""")
    c.execute("""CREATE TABLE User (
    PersonID int,
    name varchar(255),
    email varchar(255),
    password varchar(255),
    goal varchar(255) )""")
    return 'Set up'

if __name__ == '__main__':
    # app.debug = True
    app.run(host = '0.0.0.0', port = 5000)