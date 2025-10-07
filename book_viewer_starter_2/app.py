from flask import Flask, render_template, g, redirect, request

app = Flask(__name__)

def in_paragraphs(text):
    
    lst = text.split("\n\n")
    print("lst: ", lst)
    result = ""

    for sentence in lst:
        result += f"<p>{sentence}</p>"
        
    return result

app.jinja_env.filters['in_paragraphs'] = in_paragraphs

@app.before_request
def load_contents():
    with open('book_viewer/data/toc.txt', 'r') as file:
        g.contents = file.readlines()

@app.route("/")
def index():
    return render_template('home.html', contents=g.contents)

@app.route("/chapters/<page_num>")
def chapters(page_num):
    if page_num.isdigit() and 1 <= int(page_num) <= len(g.contents):
        chapter_name = g.contents[int(page_num) - 1]
        chapter_title = f"Chapter {page_num}: {chapter_name}"

        with open(f"book_viewer/data/chp{page_num}.txt", "r") as file:
            chapter_text = file.read()

        return render_template('chapter.html', contents=g.contents, chapter_text=chapter_text, chapter_title=chapter_title, page_num=page_num)
    else:
        return redirect('/')
    
@app.route('/search')
def search():
    query = request.args.get('query')
    result = []
    if query:
        for page_num in range(1, len(g.contents) + 1):
            with open(f"book_viewer/data/chp{page_num}.txt") as file:
                chapter_text = file.read()

                if query in chapter_text:
                    with open(f"book_viewer/data/toc.txt") as file:
                        chapter_titles = file.readlines()
                        chapter_title = chapter_titles[page_num - 1]
                        result.append(chapter_title)
                        
    return render_template('search.html', query=query, result=result)

@app.errorhandler(404)
def redirect_home(_error):
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=5003)