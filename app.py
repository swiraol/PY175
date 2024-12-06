from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key='secret1'

@app.before_request
def initialize_session():
    if 'lists' not in session:
        session['lists'] = []
        
@app.route("/")
def index():
    return redirect(url_for('get_lists'))

@app.route("/lists", methods=['GET'])
def get_lists():
    return render_template("lists.html", lists=session['lists'])

@app.route("/lists/new")
def add_todo():
    return render_template('new_list.html')

if __name__ == "__main__":
    app.run(debug=True, port=5003)