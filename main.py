from flask import Flask, url_for, render_template, request, redirect, flash, session
from utils.database_scripts import insert_query_user, create_table_update_contact, find_user_login, log_user_session, \
    update_user_new_login, select_all_from_table, update_user_password, get_all_states_and_cities
from flask_session import Session
import os

app = Flask(__name__)

PERMANENT_SESSION_LIFETIME = 10
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True 
app.config['SESSION_REFRESH_EACH_REQUEST'] = True 
app.config.update(SECRET_KEY=os.urandom(24))

app.config.from_object(__name__)
Session(app)

@app.route('/travelblog/about')
def about():
    return render_template('about.html', image_ruchi = "/Users/venkat/Desktop/TravelProjecr/travelprojectnew/dev-images/ruchi.jpg")

@app.route('/travelblog/home')
def site_home():
    locations = get_all_states_and_cities()['state']
    return render_template('index.html', msg='', login=url_for("login"), locations=locations, selected_state="selected_state")

# Define aliases for other URL endpoints
app.add_url_rule("/home", "home_alias", site_home)
app.add_url_rule("/welcome", "welcome_alias", site_home)
app.add_url_rule("/", "initial_alias", site_home)

def get_locationdata(selected_state, selected_city=None,  selected_category=None):
    if selected_state:
        where_clause = "state = '" + selected_state 
    if selected_city:
        where_clause = where_clause + "city = '" + selected_city 
    if selected_category:
        where_clause = where_clause + "category = '" + selected_category
    where_clause = where_clause + "';" 
    print("test", where_clause) 
    data = select_all_from_table('locations', where_clause)
    card_data = []
    for i, each in enumerate(data):
        location = {}
        location['state'] = each[1]
        location['name'] = each[2]
        location['city'] = each[3]
        location['description'] = each[4]
        location['categorytype'] = each[5]
        location['image'] = each[6]
        location['map_reflink'] = each[7]
        location['class'] = each[1] + str(i)
        card_data.append(location)
    return card_data 



@app.route('/get_filtered_data', methods=['GET'])
def get_filtered_data():
    selected_state = request.form.get('stateselector')
    selected_city = request.form.get('cityselector')
    selected_category = request.form.get('categoryselector')
    if 'username' in session:
        username = session["username"]
    else:
        username = None
    data_location  = get_all_states_and_cities()
    print(selected_city, selected_category)
    if selected_state in data_location['state']:
        session['state'] = selected_state
    else:
        selected_state = "Karnataka"
    card_data = get_locationdata(selected_state, selected_city,  selected_category)
    # Render the filtered data in a template (replace with your actual template)
    return render_template('location_select.html', username1= username, 
                           state = selected_state, 
                           data_location = data_location,
                           card_data=card_data)

   
@app.route('/travelblog/profile/location/<state>', methods=['GET', 'POST'])
def locationdetails(state):
    if 'username' in session:
        username = session["username"]
    else:
        username = None
    selected_state = request.form.get('selected_state')
    data_location  = get_all_states_and_cities()
    if selected_state in data_location['state']:
        session['state'] = selected_state
    else:
        selected_state = "Karnataka"
    card_data = get_locationdata(selected_state)
    print(data_location)
    return render_template('location_select.html', username1= username, 
                           state = selected_state, 
                           data_location = data_location,
                           card_data=card_data)

@app.route('/login')
def site_login():
    return redirect(url_for("login"))

@app.route('/travelblog/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        session['username'] = username
        password = request.form['password']
        password_db = ""
        try:
            password_db = find_user_login(username)
        except IndexError as e:    
            error = 'Invalid User! Please Register' 
        if password_db != "" and password_db.strip() != password.strip():
            print("after validation", password_db)
            error = 'Invalid User Credentials! Please try Again'
        elif password_db == "" :
            print("check none", password_db)
            redirect(url_for("register"))
        else:
            print(password_db)
            update_user_new_login(username)
            return redirect(url_for("profile", username=username))
        
    return render_template('login.html', msg=error)


@app.route('/travelblog/register', methods=['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        session['username'] = username
        password = request.form['password']
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form['email']
        try:
            password_db = find_user_login(username)
        except Exception:
            password_db = None
            insert_query_user(username=username, email=email, password=password, fname=fname, lname=lname)
        if not password_db:
            return redirect(url_for("profile", username=username))
        else:
            error = 'user already exists! please try to login!'
            return render_template('login.html', msg=error)
    elif request.method == 'post':
        error = 'please fill out the form!'
    return render_template('register.html', msg=error)


@app.route('/travelblog/forgotpassword', methods=['GET', 'POST'])
def reset_password():
    error = ''
    if request.method == 'POST' and 'username' in request.form and 'oldpassword' in request.form:
        username = request.form['username']
        session['username'] = username
        oldpassword = request.form['oldpassword']
        newpassword = request.form['newpassword']
        update_user_password(username=username, newpassword=newpassword)
        return redirect(url_for("login", username=username)) 
    return render_template('forgotpassword.html', msg = "")
    
    
@app.route('/travelblog/profile/<username>')
def profile(username):
    locations = get_all_states_and_cities()['state']
    print(locations)
    return render_template('profile.html', username1=username, locations=locations)
   
@app.route('/travelblog/contactus', methods=['GET', 'POST'])
def contactus():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        create_table_update_contact(name, email, phone, message)
        return redirect(url_for("site_home", username=name)) 
    return render_template('contact.html')

@app.route('/travelblog/logout')
def logout():
    if 'username' in session: 
        username = session['username']
        session_id = str(session.sid)
        session.pop('username', None)
        session.pop('sid', None)
        log_user_session(username, session_id)
    locations = get_all_states_and_cities()['state']
    return render_template('index.html', msg='', login=url_for("login"), locations=locations)


if __name__ == "__main__":
    with app.test_request_context("/"):
        session["key"] = "value"
    app.run(debug=True)
