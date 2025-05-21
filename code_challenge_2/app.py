from flask import Flask, render_template, redirect, g
import yaml

app = Flask(__name__)

@app.template_filter()
def show_other_users(usernames, username):
    print("usernames: ", usernames)

    return [user for user in usernames if user != username]

@app.template_filter()
def get_user_info(usernames, user_info):
    print("got user_info: ", user_info)
    total_users = len(usernames)
    print("total_users: ", total_users)
    print("g.user_data: ", g.user_data)
    user_data = g.user_data
    total_interests = 0
    for v in user_data.values():
        if not isinstance(v, dict):
            v = {}
        else:
            print("v: ", v)
            print("interests count: ", len(v.get('interests', [])))
            total_interests += len(v.get('interests', []))
            print("total_interests: ", total_interests)

    print("total_interests: ", total_interests)

    return (total_users, total_interests)

@app.before_request
def load_user_data():
    with open('users.yaml') as file:
        g.user_data = yaml.safe_load(file)

@app.route("/")
def index():

    return redirect('/users')

@app.route("/users")
def users():
    
    usernames = g.user_data.keys()

    return render_template('users.html', usernames=usernames)

@app.route("/user/<username>")
def user(username):
    print("requested username: ", username)
    user_info = g.user_data.get(username, {}) # the dictionary of user data
    print("user_info: ", user_info)
    usernames = g.user_data.keys() # the username keys
    print("usernames: ", usernames)
    
    if not isinstance(user_info, dict):
        email = "N/A"
        interests = "N/A"
        g.user_data[username] = {}
    else:
        email = user_info.get('email', "N/A") # the email string
        print("email: ", email)
        interests = ", ".join(user_info.get('interests', [])) # the interests list
        interests = interests if interests else "N/A"
        print("interests: ", interests)

    return render_template('user.html', email=email, username=username, interests=interests, usernames=usernames, user_info=user_info)

if __name__ == '__main__':
    app.run(debug=True, port=5003)