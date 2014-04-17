#
# author:shuson
#
import QueryFile
import sqlite3
from flask import Flask, request, session, g, redirect, url_for,abort, render_template,flash

app = Flask(__name__)

def get_db():
	return sqlite3.connect("files.db")

@app.route('/')
def index():
	db = get_db()
	cur = db.execute("select * from movies")
	
	movies =  cur.fetchall()
	
	return render_template('index.html',movies = movies)


if __name__== '__main__':
	QueryFile.run()
	app.run()
