from uuid import uuid4

from flask import (Flask, 
                   redirect,
                   render_template, 
                   request,
                   session,
                   url_for,
                   flash,
)

app = Flask(__name__)

app.secret_key='secret1'

@app.before_request
def initialize_session():
    session['lists'] = session.get('lists', [])

@app.route("/")
def index():

    return redirect(url_for('get_lists'))

@app.route('/lists/new')
def add_todo_list():

    return render_template('new_list.html')

@app.route('/lists', methods=["GET"])
def get_lists():
    success_msg = session.get('flash_msg', None)
    if success_msg:
        success_msg = success_msg['message']

    return render_template('lists.html', lists=session['lists'])

@app.route('/lists', methods=["POST"])
def create_list():
    title = request.form['list_title'].strip()
    session['lists'].append({
        'id': str(uuid4()),
        'title': title, 
        'todos': [],
    })
    session['flash_msg'] = {'success': True, 'message': 'The list has been added.'}
    session.modified = True

    return redirect(url_for('get_lists'))

if __name__ == "__main__":
    app.run(debug=True, port=5003)