#_____________________________________________________________________________________
from SQL_helper import *
""" Web functions """
def loged_in_success(found_user, cursor):
        """ This area is currently being testing"""
        # -----------------------------------------
        data = get_attractions(3, cursor) # For testing
        # -----------------------------------------
        return render_template('profile.html', name = found_user.name, email = found_user.email, \
        goal = found_user.goal, group = json.dumps(data))
    
def perform_login(request, cursor):
    email = request.form.get("email")
    psw = request.form.get("password")
    found_user = fetch_user_by_email_with_cursor(email, cursor)
#-----------------------------------------------------------------------
    if found_user:  # User located
        if found_user.password == psw:
            return loged_in_success(found_user, cursor)
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
        guest = User(name, email, psw, goal)
        insert_new_user_name_email_psw_goal(guest, cursor)
        return loged_in_success(guest, cursor)
    else:
        return "User Existed"