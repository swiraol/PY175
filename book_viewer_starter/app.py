from flask import Flask, render_template, g, redirect, request

def in_paragraphs(text):
    paragraphs = text.split("\n\n")
    formatted_paragraphs = [
        f'<p>{paragraph}</p>'
        for paragraph in paragraphs
        if paragraph 
    ]
    return ''.join(formatted_paragraphs)

app = Flask(__name__)
app.jinja_env.filters['in_paragraphs'] = in_paragraphs

@app.before_request
def load_contents():
    with open("book_viewer/data/toc.txt", "r") as file:
        g.contents = file.readlines()

@app.route("/")
def index():
    return render_template('home.html', contents=g.contents)

@app.route("/show/<name>")
def show(name):
    return name

@app.route("/search")
def search():
    query = request.args.get('query', '').strip()
    matches = {}
    if query:
        for index, chapter_name in enumerate(g.contents, start=1):
            with open(f"book_viewer/data/chp{index}.txt", "r") as file:
                chapter_content = file.read()

                paragraphs = chapter_content.split("\n\n")
                
                chapter_matches = []
                for i, paragraph in enumerate(paragraphs, start=1):
                    if query.lower() in paragraph.lower():
                        highlighted_paragraph = paragraph.replace(query, f"<strong>{query}</strong>")
                        chapter_matches.append((i, highlighted_paragraph.strip()))
                if chapter_matches:
                    matches[chapter_name.strip()] = chapter_matches
                
        no_matches_message = None

    if not matches:
        no_matches_message = "Sorry, no matches were found"

    return render_template('search.html', query=query, matches=matches, no_matches_message=no_matches_message)

@app.route("/chapters/<page_num>")
def chapter(page_num):
    if page_num.isdigit() and (1 <= int(page_num) <= len(g.contents)):
        chapter_name = g.contents[int(page_num) - 1]
        chapter_title = f'Chapter {page_num}: {chapter_name}'
        
        with open(f"book_viewer/data/chp{page_num}.txt") as file:
            chapter_content = file.read()
        
        return render_template('chapter.html',
                            chapter_title=chapter_title,
                            contents=g.contents,
                            chapter=chapter_content)
    else:
        return redirect('/')

@app.errorhandler(404)
def page_not_found(_error):
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=5003)