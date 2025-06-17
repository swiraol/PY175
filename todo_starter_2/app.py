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
from todos.utils import error_for_list_title, find_list_by_id, error_for_todo_title, find_todo_by_id

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
    # print("--- Inside show list ---")
    # print(f"Requesting ID: {list_id}")
    # print("Session['lists'] content at start of get_list:", session['lists'])
    print("Requesting flashes key value pair: ", session.get('_flashes', 'Key not found.'))
    all_lsts = session['lists']
    todo_lst = find_list_by_id(list_id, all_lsts)
    if todo_lst:
        return render_template('list.html', todo_lst=todo_lst)
    raise NotFound(description="List not found")

@app.route('/lists/<list_id>/todos', methods=["POST"])
def create_todo(list_id):
    todo_title = request.form.get('todo', None).strip()
    todo_lst = find_list_by_id(list_id, session['lists'])
    if not todo_lst:
        raise NotFound(description="List not found")

    error = error_for_todo_title(todo_title)
    if error:
        flash(error, "error")
        return render_template('list.html', todo_lst=todo_lst)
    print("all lists: ", session['lists'])
    print("todo_lst: ", todo_lst)
    todo_lst['todos'].append({
        'title': todo_title, 
        'id': str(uuid4()), 
        'completed': False,
    })
    
    flash("The todo was added.", "success")
    session.modified = True
    return redirect(url_for('show_list', list_id=list_id))

@app.route('/lists/<list_id>/complete_all', methods=['POST'])
def complete_all_todos(list_id):
    print("session obj: ", session['lists'])
    todo_lst = find_list_by_id(list_id, session['lists'])
    print("todo lst: ", todo_lst)
    if not todo_lst:
        raise NotFound(description="List not found")
    
    for todo in todo_lst['todos']:
        todo['completed'] = True
    
    session.modified = True
    flash("All todos are completed", "success")

    return redirect(url_for('show_list', list_id=list_id))

@app.route('/lists/<list_id>/todos/<todo_id>/toggle', methods=['POST'])
def update_todo_status(list_id, todo_id):
    todo_lst = find_list_by_id(list_id, session['lists'])

    if not todo_lst:
        raise NotFound(description="List not found.")
    
    todo_item = find_todo_by_id(todo_id, todo_lst)

    if not todo_item:
        raise NotFound(description="Todo not found.")
    
    is_completed = request.form.get('completed').lower() == 'true'
    todo_item['completed'] = is_completed

    flash('You completed an item', 'success')
    session.modified = True
    
    return redirect(url_for('show_list', list_id=list_id))

@app.route('/lists/<list_id>/todos/<todo_id>/delete', methods=["POST"])
def delete_todo(list_id, todo_id):
    todo_lst = find_list_by_id(list_id, session['lists'])
    if not todo_lst:
        raise NotFound(description="List not found.")
    
    todo_item = find_todo_by_id(todo_id, todo_lst)

    if not todo_item:
        raise NotFound(description="Todo item not found.")
    
    todo_lst['todos'] = [item for item in todo_lst['todos'] if item != todo_item]
    # print("todo_item after del: ", todo_item)
    flash("You removed a todo item", "success")
    session.modified = True
    return redirect(url_for("show_list", list_id=list_id))

if __name__ == "__main__":
    app.run(debug=True, port=5003)