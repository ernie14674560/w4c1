#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from flask import Flask, render_template
import json
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def index():

    title = []
    for n in os.listdir('files'):
        with open('files/{}'.format(n), 'r') as f:
            title_dict = json.loads(f.read())
            title.append(title_dict['title'])
    return render_template('index.html', title=title)


@app.route('/files/<filename>')
def file(filename):

    if os.path.isfile('files/{}.json'.format(filename)):
        with open('files/{}.json'.format(filename)) as f:
            contents = json.loads(f.read())
            return render_template('file.html', contents=contents, title=filename)
    else:
        return render_template('404.html'), 404
if __name__ == '__main__':
    app.run(port = 3000)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404