import os
from functools import wraps
import yaml
import bcrypt
from flask import (
    Flask,
    render_template,
    send_from_directory,
    flash,
    redirect,
    url_for,
    request,
    session
)
from markdown import markdown

app = Flask(__name__)
app.secret_key = 'secret'

def valid_credentials(username, password):
    credentials = load_user_credentials()

    if username in credentials:
        stored_password = credentials[username].encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), stored_password)
    else:
        return False
def user_signed_in():
    return 'username' in session

def required_signed_in_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if user_signed_in():
            return f(*args, **kwargs)
        else:
            flash("User is not signed in", "error")
            return redirect(url_for('show_signin_form'))
    return decorated_function

def get_data_path():
    if app.config['TESTING']:
        return os.path.join(os.path.dirname(__file__), 'tests', 'data')
    return os.path.join(os.path.dirname(__file__), 'data')

@app.route("/")
def index():
    data_dir = get_data_path()
    # print(f"Listing files from: {data_dir}")  # Debugging
    # print(f"Data path resolved to: {get_data_path()}")
    files = [os.path.basename(path) for path in os.listdir(data_dir)]
    return render_template('index.html', files=files)

@app.route("/cms/data/<filename>")
@required_signed_in_user
def file_content(filename):
    data_dir = get_data_path()
    file_path = os.path.join(data_dir, filename)
    # print(f"Looking for file in: {file_path}")
    # print(f"Data path resolved to: {get_data_path()}")


    if os.path.isfile(file_path):
        if filename.endswith('.md'):
            with open(file_path, 'r') as file:
                content = file.read()
            return markdown(content)
        else:
            return send_from_directory(data_dir, filename)
    else:
        flash(f"{filename} does not exist.")
        return redirect(url_for('index'))
    
@app.route("/cms/data/<filename>", methods=['POST'])
@required_signed_in_user
def save_file(filename):
    data_dir = get_data_path()
    file_path = os.path.join(data_dir, filename)

    updated_content = request.form['content']
    # print(f"Updated content: {repr(updated_content)}")  # Debugging

    if len(updated_content.strip()) == 0:
        # print("Validation failed: Content is empty.")  # Debugging
        flash(f"Content cannot be empty.", "error")
        return redirect(url_for('edit_file', filename=filename))
    
    # print("Validation passed: Saving file.")  # Debugging
    with open(file_path, 'w') as file:
        file.write(updated_content)
    
    flash(f"{filename} has been updated successfully", 'success')
    return redirect(url_for('index'))

@app.route('/cms/data/<filename>/edit')
@required_signed_in_user
def edit_file(filename):
    data_dir = get_data_path()
    file_path = os.path.join(data_dir, filename)

    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        return render_template('edit.html', filename=filename, content=content)
    else:
        flash(f"{filename} does not exist.")
        return redirect(url_for('index'))

@app.route('/cms/create')
@required_signed_in_user
def create_new():
    return render_template('create.html')

@app.route('/cms/create', methods=['POST'])
@required_signed_in_user
def handle_create():
    filename = request.form.get('filename')
    if not filename:
        flash("A name is required.", "error")
        return redirect(url_for('create_new'))
    
    data_dir = get_data_path()
    file_path = os.path.join(data_dir, filename)
    
    if os.path.exists(file_path):
        flash(f"{filename} already exists", 'error')
        return redirect(url_for('index'))
    else:
        # create the file
        with open(file_path, 'w') as file:
            file.write("")
        flash(f'{filename} was created', 'success')
        return redirect(url_for('index'))
    
@app.route('/cms/data/<filename>/delete', methods=['POST'])
@required_signed_in_user
def delete_file(filename):
    data_dir = get_data_path()
    file_path = os.path.join(data_dir, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f"{filename} has been deleted.", "success")
        return redirect(url_for('index'))
    else:
        flash(f"{filename} does not exist", "error")
        return redirect(url_for('index'))

@app.route('/users/signin')
def show_signin_form():
    return render_template('signin.html')

@app.route('/users/signin', methods=['POST'])
def signin():
    username = request.form.get('username')
    password = request.form.get('password')
    print(f"Username: {username}, Password: {password}")
    credentials = load_user_credentials()
    print(f"Loaded credentials: {credentials}")

    if valid_credentials(username, password):
        session['username'] = username
        flash("Welcome!", "success")
        return redirect(url_for('index'))
    else:
        flash("Invalid credentials", "error")
        return render_template('signin.html'), 422

@app.route('/users/signout', methods=['POST'])
def signout():
    session.pop('username', None)
    flash('You have been signed out', 'success')
    return redirect(url_for('index'))

def load_user_credentials():
    root_dir = os.path.dirname(__file__)
    if app.config['TESTING']:
        credentials_path = os.path.join(root_dir, 'tests', 'users.yml')
    else: 
        credentials_path = os.path.join(root_dir, 'users.yml')
    
    print(f"Loading credentials from: {credentials_path}")
    with open(credentials_path, 'r') as file:
        return yaml.safe_load(file)

if __name__ == '__main__':
    app.run(debug=True, port=5003) # Use port 8080 on Cloud9