#from flask import render_template
#from flaskexample import app

#@app.route('/')
#@app.route('/index')
#def index():
#   user = { 'nickname': 'Miguel' } # fake user
#   return render_template("index.html",
#       title = 'Home',
#       user = user)

#from flask import render_template
#from flaskexample import app
#from sqlalchemy import create_engine
#from sqlalchemy_utils import database_exists, create_database
#import pandas as pd
#import psycopg2

#username = 'harisk87'           
#host = 'localhost'
#dbname = 'birth_db'
#pswd = '2PsWrD!'
##db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
#db = create_engine('postgresql://%s:%s@localhost/%s'%(username,pswd,dbname))
#con = None
##con = psycopg2.connect(database = dbname, user = user)
#con = psycopg2.connect(database = dbname, user = username, host='localhost', password=pswd)


#@app.route('/')
#@app.route('/index')
#def index():
#    return render_template("index.html",
#       title = 'Home', user = { 'nickname': 'Miguel' },
#       )

#@app.route('/db')
#def birth_page():
#    sql_query = """                                                                       
#                SELECT * FROM birth_data_table WHERE delivery_method='Cesarean';          
#                """
#    query_results = pd.read_sql_query(sql_query,con)
#    births = ""
#    for i in range(0,10):
#        births += query_results.iloc[i]['birth_month']
#        births += "<br>"
#    return births

from flask import render_template
from flaskexample import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2

username = 'harisk87'           
host = 'localhost'
dbname = 'birth_db'
pswd = '2PsWrD!'
db = create_engine('postgresql://%s:%s@localhost/%s'%(username,pswd,dbname))
con = None
con = psycopg2.connect(database = dbname, user = username, host='localhost', password=pswd)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
       title = 'Home', user = { 'nickname': 'Miguel' },
       )

@app.route('/db')
def birth_page():
    sql_query = """                                                             
                SELECT * FROM birth_data_table WHERE delivery_method='Cesarean'\
;                                                                               
                """
    query_results = pd.read_sql_query(sql_query,con)
    births = ""
    print query_results[:10]
    for i in range(0,10):
        births += query_results.iloc[i]['birth_month']
        births += "<br>"
    return births

@app.route('/db_fancy')
def cesareans_page_fancy():
    sql_query = """
               SELECT index, attendant, birth_month FROM birth_data_table WHERE delivery_method='Cesarean';
                """
    query_results=pd.read_sql_query(sql_query,con)
    births = []
    for i in range(0,query_results.shape[0]):
        births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['attendant'], birth_month=query_results.iloc[i]['birth_month']))
    return render_template('cesareans.html',births=births)

