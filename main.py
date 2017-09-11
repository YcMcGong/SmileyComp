"""
Copyright (cursor) <2017> <Yicong Gong>

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

from flask import Flask, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
# import flask_login
from SQL_helper import *
# from helper import image_resize, address_to_gps, gps_to_address
from helper import *
import MySQLdb
import config
import json
import os
import storage

"""Hard coded part"""
admin_code = '1234567890'

app = Flask(__name__)
""" For local server """
# UPLOAD_FOLDER = '/static/uploads/images'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # For local server

app.secret_key = 'testing_secret_key'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

""" Uncomment the 1st for local DB and the 2nd for Google cloud SQL"""
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test101.db'        # Local testing
app.config.from_object(config)                                               # Deployment
db = config.connect_to_cloudsql()
cursor = db.cursor()
cursor.execute("""USE Smiley""") # Specifies the name of DB

def reconnect_to_sql():
    db = config.connect_to_cloudsql()
    cursor = db.cursor()
    cursor.execute("""USE Smiley""") # Specifies the name of DB 
    pass

""" Login related---------------------------------------------------------"""
class Login(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    user = Login()
    user.id = email
    return user
#_____________________________________________________________________________
""" Function calls"""
""" Web functions """
def loged_in_success(current_user, cursor):
    """ This area is currently being testing"""
    # -----------------------------------------
    found_user = fetch_user_by_email_with_cursor(current_user.id, cursor)
    data = get_attractions(3, cursor) # For testing
    # # -----------------------------------------
    return render_template('profile.html', name = found_user.name, email = found_user.email, \
    goal = found_user.goal, group = json.dumps(data))
    
def perform_login(request, cursor):
    email = request.form.get("email")
    psw = request.form.get("password")
    found_user = fetch_user_by_email_with_cursor(email, cursor)
#-----------------------------------------------------------------------
    if found_user:  # User located
        if found_user.password == psw:
            # return loged_in_success(found_user, cursor)
            user = Login()
            user.id = email
            flask_login.login_user(user)
            return redirect(url_for('protected'))
        else:   
            return "Password incorrect"
    else:
        return "No User found"

def perform_sign_up(request, cursor):
    name = request.form.get("name")
    email = request.form.get("email")
    psw = request.form.get("password")
    goal = request.form.get("goal")
#--------------------------------------------------------------
    found_user = fetch_user_by_email_with_cursor(email, cursor)
#--------------------------------------------------------------
    if found_user==None:  # User not located
        # return loged_in_success(guest, cursor)
        user = Login()
        user.id = email
        guest = User(name, email, psw, goal)
        insert_new_user_name_email_psw_goal(guest, cursor)
        flask_login.login_user(user)
        return redirect('/protected')
    else:
        return "User Existed"

#____________________________________________________________________________
""" The following is for event handlers"""
@app.route('/protected')
@flask_login.login_required
def protected():
    return loged_in_success(flask_login.current_user, cursor)

@app.route('/')
@app.route('/welcome')
def front_page():
    reconnect_to_sql()
    if flask_login.current_user.is_authenticated:
        return redirect(url_for('protected'))
    else:
        return render_template('front_page.html')

@app.route('/login_post',methods=['GET', 'POST'])
def login_post():
    if request.method == 'POST':
        return perform_login(request, cursor)
    else:
        return "Invalid Request"

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up_page():
    return render_template('sign_up.html')

@app.route('/sign_up_post', methods=['GET', 'POST'])
def sign_up_post():
    if request.method == 'POST':
        return perform_sign_up(request, cursor)
    else:
        return "Invalid Request"

@app.route('/create_new_place')
@flask_login.login_required
def create_a_new_place():
    return render_template('create_place.html')

#--------------------------------------------------------------------------
@app.route('/create_new_place_post', methods=['GET', 'POST'])
@flask_login.login_required
def create_a_new_place_post():
    
    code = request.form.get('code')

    if code == admin_code:
        name = request.form.get('name')
        # marker = upload_image_file(request.files.get('cover'), is_marker = True)
        image_file = request.files.get('cover')
        # image_file = request.files['cover']
        cover = upload_image_file(image_file, is_marker = False)
        marker = upload_image_file(image_file, is_marker = True)
        # if request.form.get('address'):
        #     location = address_to_gps(request.files.get('address'))
        #     lat = location[0]
        #     lng = location[1]
        # else:
        #     lat = request.files.get('lat')
        #     lng = request.files.get('lng')
        location = address_to_gps(request.form.get('address'))
        lat = location[0]
        lng = location[1]
        description = request.form.get('description')

        # Insert the new attraction to SQL
        attraction = Attraction(name, marker, cover, lat, lng, description)
        insert_new_attraction(attraction, cursor)
        flash('file submitted')
        return redirect('/protected')
    
    else:
        return "Only admin can upload attraction"

""" For local server"""
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def upload_file(request):
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'cover' not in request.files:
#             print('no file')
#             flash('No file part')
#             return redirect('/create_new_place')
#         file = request.files['cover']
#         # if user does not select file, browser also
#         # submit a empty part without filename
#         print(file.filename)
#         if file.filename == '':
#             print('no name')
#             flash('No selected file')
#             return redirect('/create_new_place')
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             print('loop entered')
#             return filename

# [START upload_image_file]
def upload_image_file(file, is_marker = False):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not file:
        return None

    if is_marker:
        file_resize = image_resize(file)
        public_url = storage.upload_file(
            file_resize.read(),
            file.filename,
            file.content_type
        )

    else:
        public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
        )

    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)

    return public_url
# [END upload_image_file]
#--------------------------------------------------------------------------
""" Each place profile """
@app.route('/places/<name>', methods = ['GET', 'POST'])
def places(name):
    return place_page(name)

def place_page(name):
    data = look_up_place_data(name, cursor)
    address = gps_to_address(float(data['lat']), float(data['lng']))
    return render_template('place.html', name = data['name'], address = address, 
        cover = data['cover'], description = data['description'])
#--------------------------------------------------------------------------
@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect('/welcome')

@app.route('/init_all_this_is_a_secret_key_not_posting_here')
def init():

    cursor.execute("""DROP TABLE User""")
    cursor.execute("""CREATE TABLE User (
    PersonID int,
    name varchar(255),
    email varchar(255),
    password varchar(255),
    goal varchar(255) )""")

    cursor.execute("""DROP TABLE Attraction""")
    cursor.execute("""CREATE TABLE Attraction (
    id varchar(255),
    name varchar(255),
    marker varchar(255),
    cover varchar(255),
    lat varchar(255),
    lng varchar(255),
    description varchar(255) )""")

    return 'Set up'

if __name__ == '__main__':
    # app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
