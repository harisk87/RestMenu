from flask import render_template
from flask import request
from flaskexample import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from a_Model import ModelIt
import pandas as pd
import psycopg2
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse



username = 'harisk87'
host = 'localhost'
dbname = 'rest_db'
pswd = '2PsWrD!'
db = create_engine('postgresql://%s:%s@localhost/%s'%(username,pswd,dbname))
con = None
con = psycopg2.connect(database = dbname, user = username, host='localhost', password=pswd)

@app.route('/input')
def rest_input():
    return render_template("input.html") #SENDS THE BROWSER RESULTS

@app.route('/output') #DECORATER
def rest_output():
  #pull 'menu_item' from input field and store it
  rest_name = request.args.get('rest_name')
  menu_item = request.args.get('menu_item')

  pd_rest_table = pd.read_pickle('all_amrests_df')

  idx = pd_rest_table[(pd_rest_table['Restaurant Name'] == rest_name) & (pd_rest_table['Menu Item'] == menu_item)].index.values[0]

  tf_idf_mat = pickle.load( open( 'tfidfmat.pickle', "rb" ) )
  cosine_similarities = cosine_similarity(tf_idf_mat[idx], tf_idf_mat).flatten()

  related_food_idcs = cosine_similarities.argsort()[::-1][1:11]
  print related_food_idcs

  rests = []
  for i in related_food_idcs:
  	menu_print = pd_rest_table.iloc[i]['Menu Item']
	desc_print = pd_rest_table.iloc[i]['Item Description']
	name_print = pd_rest_table.iloc[i]['Restaurant Name']
	price_print = pd_rest_table.iloc[i]['Price']
  	rests.append(dict(menu_item=menu_print, desc=desc_print, name=name_print, price=price_print) )

  print rests
  return render_template("output.html",rests=rests,rest_name = rest_name, menu_item = menu_item)


#
#	#Load the tf-idf matrix for the stored food
#	with open('tfidfmat.pickle') as f:  # Python 3: open(..., 'rb')
#  		tfidfmat = pickle.load(f)
#
#	#Get




    #just select the Cesareans  from the birth dtabase for the month that the user inputs
  #query = "SELECT index, attendant, birth_month FROM birth_data_table WHERE delivery_method='Cesarean' AND birth_month='%s'" % food
#  query = """ SELECT * FROM rest_table"""
#  print query
#  query_results=pd.read_sql_query(query,con)
#  print query_results
#  rests = []
#  for i in range(300,350):#query_results.shape[0]
#	menu_print = query_results.iloc[i]['Menu Item']
#	desc_print = query_results.iloc[i]['Item Description']
#	name_print = query_results.iloc[i]['Restaurant Name']
#	price_print = query_results.iloc[i]['Price']

##	menu_print = encoding_hack(menu_print)
##	desc_print = encoding_hack(desc_print)
##	name_print = encoding_hack(name_print)
##	price_print = encoding_hack(price_print)

#    	rests.append(dict(menu_item=menu_print, desc=desc_print, name=name_print, price=price_print) )

#  the_result = 0
  #, rests = rests, the_result = the_result)

#def encoding_hack(text):
#	text_int = text.encode("utf-8")
#	out_text = text_int.decode("utf-8").encode('ascii','ignore')
#	return out_text
