from flask import render_template
from flask import request
from flaskexample import app
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse


@app.route('/')
def start_page():
    rest_name_dict = []
    pd_rest_table = pd.read_pickle('all_amrests_df')
    rest_name_list = sorted(pd_rest_table['Restaurant Name'].unique().tolist())
    return render_template('master_restname.html',rest_name_list = rest_name_list)

@app.route('/mid_page', methods =['POST'])
def mid_page():
    print request.form
    rest_name = request.form['rest_name']
    pd_rest_table = pd.read_pickle('all_amrests_df')
    menu_item_list = pd_rest_table[pd_rest_table['Restaurant Name']==rest_name]['Menu Item'].tolist()
    menu_item_list = [s.decode('utf-8') for s in menu_item_list]
    return render_template('master_menu_item.html',menu_item_list = menu_item_list,rest_name=rest_name)

@app.route('/result', methods =['POST'])
def result():
    print request.form
    rest_name = request.form['rest_name']
    menu_item = request.form['menu_item']
    print rest_name
    pd_rest_table = pd.read_pickle('all_amrests_df')

    pd_rest_table['Menu Item'] = [s.decode('utf-8') for s in pd_rest_table['Menu Item']]
    pd_rest_table['Item Description'] = [s.decode('utf-8') for s in pd_rest_table['Item Description']]
    #print pd_rest_table.loc[rest_name].index
    idx = pd_rest_table[(pd_rest_table['Restaurant Name'] == rest_name) & (pd_rest_table['Menu Item'] == menu_item)].index[0]

    tf_idf_mat = pickle.load( open( 'tfidfmat.pickle', "rb" ) )
    cosine_similarities = cosine_similarity(tf_idf_mat[idx], tf_idf_mat).flatten()
    related_food_idcs = cosine_similarities.argsort()[::-1][1:6]
    #
    result_dict = []
    for i in related_food_idcs:
        menu_print = pd_rest_table.iloc[i]['Menu Item']
        desc_print = pd_rest_table.iloc[i]['Item Description']
        name_print = pd_rest_table.iloc[i]['Restaurant Name']
        price_print = pd_rest_table.iloc[i]['Price']
        result_dict.append(dict(menu_item=menu_print, desc=desc_print, name=name_print, price=price_print) )

    return render_template('result.html',rest_name=rest_name, menu_item=menu_item, result_dict = result_dict)
