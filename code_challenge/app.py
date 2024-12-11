'''
# homepage

- user's names are linked to user pages

# user page
- display email address
- display interests that are comma-delimited
- at the bottom, link to other user pages

# add layout
- at the bottom of every page, display a message: "There are 3 users with a total of 9 interests."
    - update the message to determine the number of users and interests based on the content of the YAML file. Use a view helper method, total_interests, to determine the total number of interests across all users.
    - test this case by adding a new user to the yaml file

'''

from flask import Flask, render_template, redirect, url_for
import yaml

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

with open('users.yaml', 'r') as file:
    data = yaml.safe_load(file)

def total_interests(data):
    return sum(len(user['interests']) for user in data.values())

@app.route('/')
def index():
    return redirect(url_for('users_list'))
    

@app.route('/users')
def users_list():
    users = data.keys()
    total_users = len(users)
    total_interests_count = total_interests(data)
    return render_template("index.html", users=users, total_users=total_users, total_interests=total_interests_count)

@app.route('/users/<username>')
def user(username):
    user_details = data.get(username)
    if not user_details:
        return redirect(url_for('users_list'))
    
    users = data.keys()
    total_users = len(users)
    total_interests_count = total_interests(data)

    return render_template("user.html", username=username, user_details=user_details, other_users=[name for name in data if name != username], total_users=total_users, total_interests=total_interests_count)

if __name__ == '__main__':
    app.run(debug=True, port=5003)






