from flask import Flask, render_template, g, redirect, request
import re

app = Flask(__name__)
print(f"The value of __name__ in this module is {__name__}")

def in_paragraphs(text):
    return text.split('\n\n')

def view_helper(text, query):
    result = text.split(query)
    print("result: ", result)
    query = f"<strong>{query}</strong>"
    
    return query.join(result)


app.jinja_env.filters['view_helper'] = view_helper

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
    print("page_num: ", page_num)
    if page_num.isdigit() and 1 <= int(page_num) <= len(g.contents):
        with open(f"book_viewer/data/chp{page_num}.txt", 'r') as file:
            paragraphs = file.read()
    
        return render_template('chapter.html', 
                            chapter_paragraphs=paragraphs, 
                            chapter_titles=g.contents,
                            page_num=int(page_num))
    else:
        return redirect('/')

@app.route("/search", endpoint='search')
def search():
    query = request.args.get('query', '')
    results = {}
    chp_count = len(g.contents)
    if query:
        for chp_num in range(1, chp_count + 1):
            temp_lst = []
            title = g.contents[chp_num - 1]
            with open(f"book_viewer/data/chp{chp_num}.txt") as file:
                single_string = file.read()
                paragraphs = single_string.split("\n\n")
                for index, paragraph in enumerate(paragraphs, start=1):
                    if query.casefold() in paragraph.casefold():
                        temp_lst.append([index, paragraph])
                print("temp list: ", temp_lst)

                if temp_lst:
                    print("temp_lst: ", temp_lst)
                    results[chp_num] = {
                        'title': title,
                        'paragraphs': temp_lst
                    }
                print("results: ", results)
    
    return render_template('search.html', query=query, results=results, chapter_titles=g.contents)

@app.errorhandler(404)
def page_not_found(error):
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=5003)