#coding: utf-8
from flask import Flask, request
from flask import render_template
from musicSearch import Search

app = Flask(__name__)
ms = Search()

@app.route('/')
def music():
    return render_template('index.html', filename=u'朴树-平凡之路.mp3')

@app.route('/query', methods=['POST'])
def query():
    if request.method == 'POST':
        query_words = request.form['query']
        q_acc = ms.parser.parse(query_words)
        res_acc = ms.searcher.search(q_acc)
        filename = res_acc[0]['title']
        filename = filename[:-4] + '.mp3'
        return render_template('index.html', filename=filename)
    else:
        render_template('index.html', filename=u'朴树-平凡之路.mp3')

if __name__ == '__main__':
    app.run(debug=True)