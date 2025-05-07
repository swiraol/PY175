from flask import Flask, render_template

app = Flask(__name__)
print(f"The value of __name__ in this module is {__name__}")

@app.route("/")
def index():
    with open('book_viewer/data/toc.txt', 'r') as file:
        chapter_titles = file.readlines()

    return render_template('home.html', chapter_titles=chapter_titles)

@app.route("/chapters/<page_num>")
def chapter(page_num):
    with open('book_viewer/data/toc.txt', 'r') as file:
        chapter_titles = file.readlines()
        print("chapter_titles: ", chapter_titles)
    with open(f"book_viewer/data/chp{page_num}.txt", 'r') as file:
        chapter_content = file.readlines()
    
    return render_template('chapter.html', 
                           chapter_content=chapter_content, 
                           chapter_titles=chapter_titles,
                           page_num=int(page_num))

if __name__ == "__main__":
    app.run(debug=True, port=5003)