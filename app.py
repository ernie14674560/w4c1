#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/你創建的數據庫名稱'
engine = SQLAlchemy.create_engine('mysql://root@localhost/你創建的數據庫名稱')
Session = SQLAlchemy.sessionmaker(bind=engine)
session = Session()
db = SQLAlchemy(app)


class File(db.Model):
    __tablename__ == 'files'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    content = db.Column(db.Text)
    category = db.relationship('Category', backref=db.backref('files', lazy='dynamic'))

    def __init__(self, title, category, content, created_time=None):
        self.title = title
        if created_time is None:
            created_time = datetime.utcnow()
        self.created_time = created_time
        self.category = category
        self.content = content


class Category(db.Model):
    __tablename__ == 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    files = db.relationship('File')
    def __init__(self, name):
        self.name = name

def insert_datas():
    db.create_all()
    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello Java', datetime.utcnow(), java, 'File Content - Java is cool!')
    file2 = File('Hello Python', datetime.utcnow(), python, 'File Content - Python is cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()

@app.route('/')
def index():
    title = session.query(files.id, files.title).all()
    return render_template('index.html', title=title)


@app.route('/files/<file_id>')
def file(file_id):
    contents = session.query.get_or_404(files.id, files.content, files.created_time, files.category).all()
    return render_template('file.html', contents=contents)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(port=3000)
