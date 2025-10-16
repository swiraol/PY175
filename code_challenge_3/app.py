from flask import Flask, render_template, g
import yaml 

app = Flask(__name__)

def get_total_interests(lst):
    return len(lst)

@app.before_request
def load_contents():
    with open('users.yaml', 'r') as file:
        g.storage = yaml.safe_load(file)
        g.users = [user for user in g.storage]

        g.interest_count = 0
        for v in g.storage.values():
            g.interest_count += get_total_interests(v['interests'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users/<name>')
def user(name):
    for k, v in g.storage.items():
        print("g.storage.items(): ", g.storage.items())
        if k == name:
            email = v['email']
            interests = v['interests']
                
    return render_template('user.html', name=name, email=email, interests=interests)

if __name__ == '__main__':
    app.run(debug=True, port=5003)