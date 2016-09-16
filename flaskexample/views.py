from flask import render_template
from flask import request
from flaskexample import app
import pandas as pd


@app.route('/')

@app.route('/index')
def index():
    return render_template('master.html')

@app.route('/go')
def go():
    query = request.args.get('query', '')
    return render_template(
        'go.html',
        query = query,
    )
