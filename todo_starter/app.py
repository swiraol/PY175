from uuid import uuid4 
from functools import wraps
import os
from flask import (
    Flask, 
    render_template, 
    redirect, 
    url_for, 
    session, 
    request,
    flash,
)
from todos.utils import error_for_list_title, error_for_todo_title, find_list_by_id, todos_remaining, is_list_completed, sort_items, is_todo_completed, find_todo_by_id, mark_all_completed
from werkzeug.exceptions import NotFound

app = Flask(__name__)
app.secret_key='secret1'

def require_list(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        list_id = kwargs.get('list_id')
        lst = find_list_by_id(list_id, session['lists'])
        if not lst:
            raise NotFound(description="List not found")
        return f(lst=lst, *args, **kwargs)
    
    return decorated_function

def require_todo(f):
    @wraps(f)
    @require_list
    def decorated_function(lst, *args, **kwargs):
        todo_id = kwargs.get('todo_id')
        todo = find_todo_by_id(todo_id, lst[['todos']])
        if not todo:
            raise NotFound(description="Todo not found")
        return f(lst=lst, todo=todo, *args, **kwargs)
    
    return decorated_function

@app.context_processor
def list_utilities_processor():
    return dict(is_list_completed=is_list_completed)

@app.before_request
def initialize_session():
    if 'lists' not in session:
        session['lists'] = []

@app.route("/")
def index():
    return redirect(url_for('get_lists'))

@app.route("/lists", methods=['GET'])
def get_lists():
    lists = sort_items(session['lists'], is_list_completed)
    return render_template("lists.html", lists=lists, todos_remaining=todos_remaining)

@app.route("/lists", methods=['POST'])
def create_list():
    title = request.form['list_title'].strip()
    error = error_for_list_title(title, session['lists'])
    if error:
        flash(error, "error")
        return render_template('new_list.html', title=title)
    
    session['lists'].append({
            'id': str(uuid4()), 
            'title': title, 
            'todos': [],
    })

    session.modified = True
    flash("You're a rockstar. The list has been created.", "success")
    return redirect(url_for('get_lists'))

@app.route("/lists/new")
def add_todo():
    return render_template('new_list.html')

@app.route("/lists/<list_id>")
@require_list
def show_list(lst, list_id):
    
    lst['todos'] = sort_items(lst['todos'], is_todo_completed)
    return render_template('list.html', lst=lst)

@app.route("/lists/<list_id>/todos", methods=['POST'])
@require_list
def create_todo_item(lst, list_id):

    title = request.form['todo'].strip()
    error = error_for_todo_title(title, lst)

    if error:
        flash(error, "error")
        return redirect(url_for('show_list', list_id=list_id, invalid_title=title))

    lst['todos'].append({'id': str(uuid4()), 'title': title, 'completed': False})
    session.modified = True
    flash("New todo added successfully!", "success")
    return redirect(url_for('show_list', list_id=list_id))

@app.route('/lists/<list_id>/todos/<todo_id>/toggle', methods=['POST'])
def toggle_todo_status(list_id, todo_id):
    # Find the list and the todo, then toggle its completed status.
    
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound
    for todo in lst['todos']:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            session.modified = True
            flash("Todo status updated successfully", "success")
            return redirect(url_for("show_list", list_id=list_id))
    raise NotFound

@app.route('/lists/<list_id>/todos/<todo_id>/delete', methods=['POST'])
def delete_todo_item(lst, todo, list_id, todo_id):
    # Find the list, locate the todo by ID, and remove it.
    delete_todo_by_id(todo_id, lst)
    session.modified = True
    flash("Todo item was removed", "success")   
    return redirect(url_for('show_list', list_id=list_id))

@app.route('/lists/<list_id>/complete_all', methods=['POST'])
@require_list
def complete_all_todos(lst, list_id):
    # Find the list and set all todos' "completed" field to True.
    mark_all_completed(lst)
    session.modified = True
    flash("All todos have been completed", "success")
    return redirect(url_for('show_list', list_id=list_id))

@app.route('/lists/<list_id>/edit')
def edit_list(list_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound
    
    return render_template('edit_list.html', lst=lst)

@app.route('/lists/<list_id>/delete', methods=['POST'])
@require_list
def delete_list(lst, list_id):
    session['lists'] = [d for d in session['lists'] if d['id'] != list_id]
    session.modified = True
    flash("The list has been deleted", "success")
    return redirect(url_for('get_lists'))

@app.route('/lists/<list_id>', methods=['POST'])
@require_list
def edit_list_title(lst, list_id):
    return redirect(url_for('show_list', list_id=list_id))

@require_list
def update_list(lst, list_id):
    title = request.form["list_title"].strip()
    error = error_for_list_title(title, session['lists'])
    if error:
        flash(error, "error")
        return render_template('edit_list.html', lst=lst, title=title)

    lst['title'] = title
    flash("The list has been updated.", "success")
    session.modified = True
    return redirect(url_for('show_list', list_id=list_id))

if __name__ == "__main__":
    if os.environ.get('FLASK_ENV') == 'production':
        app.run(debug=False)
    else:
        app.run(debug=True, port=5003)