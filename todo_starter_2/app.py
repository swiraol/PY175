from uuid import uuid4

from flask import (Flask, 
                   redirect,
                   render_template, 
                   request,
                   session,
                   url_for,
                   flash,
)
from werkzeug.exceptions import NotFound
from todos.utils import error_for_list_title, find_list_by_id

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

    return render_template('lists.html', lists=session['lists'])

@app.route('/lists', methods=["POST"])
def create_list():
    title = request.form.get('list_title', None).strip()
    lists = session['lists']

    error = error_for_list_title(title, lists)

    if error:
        flash(error, "error")
        return render_template('new_list.html', title=title)
    
    session['lists'].append({
            'id': str(uuid4()),
            'title': title, 
            'todos': [],
    })
        
    flash('The list has been added.', 'success')
    session.modified = True
    return redirect(url_for('get_lists'))

@app.route('/lists/<list_id>', methods=["GET"])
def show_list(list_id):
    all_lsts = session['lists']
    todo_lst = find_list_by_id(list_id, all_lsts)
    if todo_lst:
        return render_template('list.html', todo_lst=todo_lst)
    raise NotFound(description="List not found")

if __name__ == "__main__":
    app.run(debug=True, port=5003)