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

    return render_template('lists.html', lists=session['lists'])

@app.route('/lists', methods=["POST"])
def create_list():
    title = request.form.get('list_title', None).strip()

    if any(title.casefold() == lst['title'].casefold() for lst in session['lists']):
        flash("You already have a list title by that name.", "error")
        return render_template('new_list.html', title=title)
    
    if 1 <= len(title) <= 100:
        session['lists'].append({
                'id': str(uuid4()),
                'title': title, 
                'todos': [],
        })
            
        flash('The list has been added.', 'success')
        session.modified = True
        return redirect(url_for('get_lists'))
    
    flash("Your title must be 100 characters or less.", "error")
    return render_template('new_list.html', title=title)
if __name__ == "__main__":
    app.run(debug=True, port=5003)