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
        if res_acc:
            filename = res_acc[0]['title']
            filename = filename[:-4] + '.mp3'
            return render_template('index.html', filename=filename)
        else:
            cx = {}
            s = ms.analyzer(query_words)
            for t in s:
                q = ms.parser.parse(t.text)
                results = ms.searcher.search(q)
                for res in results:
                    if cx.has_key(res['title']):
                        cx[res['title']] += 1
                    else:
                        cx[res['title']] = 1
            cx = sorted(cx.iteritems(), key=lambda d:d[1], reverse = True)
            filename = cx[0][0]
            filename = filename[:-4] + '.mp3'
            return render_template('index.html', filename=filename)
    else:
        render_template('index.html', filename=u'朴树-平凡之路.mp3')

if __name__ == '__main__':
    app.run(debug=True)