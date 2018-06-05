#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from datetime import datetime


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'
db = SQLAlchemy(app)
client = MongoClient('127.0.0.1', 27017)
mdb = client.shiyanlou

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    content = db.Column(db.Text)
    category = db.relationship('Category', uselist=False)

    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

    # 向文章添加標籤
    def add_tag(self, tag_name):
        # 為當前文章添加 tag_name 標籤存入到 MongoDB
        tag = {'id': self.id, 'tag': tag_name}
        mdb.tag.insert_one(tag)
        pass

    # 移除標籤
    def remove_tag(self, tag_name):
        # 從 MongoDB 中刪除當前文章的 tag_name 標籤
        mdb.tag.deleteOne({'id': self.id})
        pass

    # 標籤列表
    @property
    def tags(self):
        # 讀取 mongodb，返回當前文章的標籤列表
        result = []
        cursor = mdb.tag.find({'id': self.id})
        for n in cursor:
            result.append(n['tag'])
        return result



class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    files = db.relationship('File')
    def __init__(self, name):
        self.name = name


@app.route('/')
def index():
    files = File.query.all()
    return render_template('index.html', files=files)


@app.route('/files/<file_id>')
def file(file_id):
    contents = File.query.get_or_404(file_id)
    return render_template('file.html', contents=contents)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(port=3000)
