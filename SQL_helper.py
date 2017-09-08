"""This helper is to wrap the SQL queries as regular python fuction,
   so that it looks neat"""
from flask import Flask, render_template, request, redirect
import json
#___________________________________________________________________
""" Structure Data"""
class User():
    
    def __init__(self, name, email, password, goal):
        self.name = name
        self.email = email
        self.password = password
        self.goal = goal

    def __repr__(self):
        return '<User %r>' % self.name

def Attraction_create(Lat, Lng, image, url):
    return {'Lat': Lat, 'Lng': Lng, 'image': image, 'url': url}

#___________________________________________________________________________________
""" Access SQL"""
def get_attractions(id, cursor): # Return the attractions for a specific user
    data = []
    data.append(Attraction_create(33.7490, -84.3880, 
    'http://v3.scout-site.com/perez-landscaping/wp-content/uploads/sites/1070/2016/03/perez-landscaping-lakewood-nj-tile-installation-patio-pavers-3-1.jpg',
    'http://www.google.com'))
    return data

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

