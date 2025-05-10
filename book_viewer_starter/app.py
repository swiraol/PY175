from flask import Flask, render_template, g, redirect
import re

app = Flask(__name__)
print(f"The value of __name__ in this module is {__name__}")

def in_paragraphs(text):
    paragraphs = text.split('\n\n')
    
    paragraphs = [f"<p>{paragraph}</p>" for paragraph in paragraphs]
    return "".join(paragraphs)

app.jinja_env.filters['in_paragraphs'] = in_paragraphs

@app.before_request
def load_contents():
    with open("book_viewer/data/toc.txt", "r") as file:
        g.contents = file.readlines()

@app.route("/")
def index():
    return render_template('home.html', chapter_titles=g.contents)

@app.route("/chapters/<page_num>")
def chapter(page_num):
    if page_num.isdigit() and 1 <= int(page_num) <= len(g.contents):
        with open(f"book_viewer/data/chp{page_num}.txt", 'r') as file:
            chapter_content = file.read()
    
        return render_template('chapter.html', 
                            chapter_paragraphs=chapter_content, 
                            chapter_titles=g.contents,
                            page_num=int(page_num))
    else:
        return redirect('/')

@app.errorhandler(404)
def page_not_found(error):
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=5003)