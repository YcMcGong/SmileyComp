"""This helper is to wrap the SQL queries as regular python fuction,
   so that it looks neat"""
from flask import Flask, render_template, request, redirect, url_for
import flask_login
import json
#___________________________________________________________________
""" Structure Data"""
class User(flask_login.UserMixin):
    
    def __init__(self, name, email, password, goal):
        self.name = name
        self.email = email
        self.password = password
        self.goal = goal

    def __repr__(self):
        return '<User %r>' % self.name

class Attraction():
    
    def __init__(self, name, marker, cover, lat, lng, description):
        self.id = marker
        self.name = name
        self.marker = marker
        self.cover = cover
        self.lat = lat
        self.lng = lng
        self.description = description

    def __repr__(self):
        return '<User %r>' % self.name

def Attraction_create(Lat, Lng, image, url):
    return {'Lat': Lat, 'Lng': Lng, 'image': image, 'url': url}

#___________________________________________________________________________________
""" Access SQL"""
def get_attractions(id, cursor): # Return the attractions for a specific user
    all_markers = read_all_marker(cursor)
    data = []
    for result in all_markers:
        data.append(Attraction_create(result[0], result[1], result[2], '/places/'+result[3]))
    return data
    # data = []
    # data.append(Attraction_create(33.7490, -84.3880, 
    # 'http://v3.scout-site.com/perez-landscaping/wp-content/uploads/sites/1070/2016/03/perez-landscaping-lakewood-nj-tile-installation-patio-pavers-3-1.jpg',
    # 'http://www.google.com'))
    # return data

def fetch_user_by_email_with_cursor(value, cursor):
    # cursor.execute("""SELECT name, email, password, goal FROM User WHERE email = %s""", (email,))
    cursor.execute("""SELECT name, email, password, goal FROM User WHERE email = %s""", (value,))
    info = cursor.fetchone()
    if info:
        found_user = User(info[0], info[1], info[2], info[3])
    else: found_user = None
    return found_user

def insert_new_user_name_email_psw_goal(User, cursor):
    cursor.execute("""INSERT INTO User (name, email, password, goal) VALUES (%s, %s, %s, %s)""", 
        (User.name, User.email, User.password, User.goal))
    cursor.execute("""COMMIT""")
    pass

def insert_new_attraction(attraction, cursor):
    cursor.execute("""INSERT INTO Attraction (id, name, marker, cover, lat, lng, description) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
        (attraction.id, attraction.name, attraction.marker, attraction.cover, 
         attraction.lat, attraction.lng, attraction.description))
    cursor.execute("""COMMIT""")
    pass

def read_all_marker(cursor):
    cursor.execute("""SELECT lat, lng, marker, name FROM Attraction""")
    all_markers = cursor.fetchall()
    # print(all_markers)
    return all_markers

def look_up_place_data(name, cursor):
    cursor.execute("""SELECT name, lat, lng, cover, description FROM Attraction WHERE name = %s""", (name,))
    data = cursor.fetchone()
    return_data = {'name':data[0], 'lat': data[1], 'lng': data[2], 'cover': data[3], 'description' : data[4]}
    return return_data
