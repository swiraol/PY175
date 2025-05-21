from flask import Flask, render_template, redirect, g
import yaml

app = Flask(__name__)

@app.template_filter()
def show_other_users(usernames, username):
    """Returns a list of other users"""
    return [user for user in usernames if user != username]

@app.template_filter()
def get_user_info(usernames):
    """Returns a tuple of counts for total users and interests"""
    total_users = len(usernames)
    total_interests = get_total_interests()

    return (total_users, total_interests)

def get_total_interests():
    """A helper function to calculate total interests of all users"""
    user_data = g.user_data
    total_interests = 0
    for v in user_data.values():
        if not isinstance(v, dict):
            v = {}
        else:
            total_interests += len(v.get('interests', []))
    
    return total_interests

@app.before_request
def load_user_data():
    """Loads the yaml file for the lifecycle of a request"""
    with open('users.yaml') as file:
        g.user_data = yaml.safe_load(file)

@app.route("/")
def index():
    """Redirects to the /users page"""
    return redirect("url_for('users')")

@app.route("/users")
def users():
    """Shows all the users on the page"""
    usernames = g.user_data.keys()

    return render_template('users.html', usernames=usernames)

@app.route("/user/<username>")
def user(username):
    """Shows the user's email and interests data"""
    user_info = g.user_data.get(username, {}) # the dictionary of user data
    usernames = g.user_data.keys() # the username keys
    
    if not isinstance(user_info, dict):
        email = "N/A"
        interests = "N/A"
        g.user_data[username] = {}
    else:
        email = user_info.get('email', "N/A") # the email string
        interests = ", ".join(user_info.get('interests', [])) # the interests list
        interests = interests if interests else "N/A"

    return render_template('user.html', email=email, username=username, interests=interests, usernames=usernames, user_info=user_info)

if __name__ == '__main__':
    app.run(debug=True, port=5003)