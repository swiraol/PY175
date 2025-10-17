from flask import Flask, render_template, g, redirect, url_for
import yaml 

app = Flask(__name__)

def get_total_interests(dict):
    result_lst = []
    for v in dict.values():
        for interest in v['interests']:
            result_lst.append(interest)
    return len(result_lst)

@app.before_request
def load_contents():
    with open('users.yaml', 'r') as file:
        g.storage = yaml.safe_load(file)
        g.users = [user for user in g.storage.keys()]
        g.interest_count = get_total_interests(g.storage)

@app.route('/')
def index():
    return redirect(url_for('users'))

@app.route('/users')
def users():
    return render_template('index.html')

@app.route('/users/<name>')
def user(name):
    user_info = g.storage.get(name)
    if not user_info:
        return redirect(url_for('users'))
                
    return render_template('user.html', name=name, email=user_info['email'], interests=user_info['interests'])

if __name__ == '__main__':
    app.run(debug=True, port=5003)