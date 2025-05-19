from flask import Flask, render_template, redirect, g
import yaml

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True, port=5003)