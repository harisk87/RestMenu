from flask import render_template
from flask import request
from flaskexample import app
import pandas as pd
import cPickle as pickle
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

#@app.route('/index')
@app.route('/')
def start_page():
  name_and_addr_list = pickle.load(open( "name_and_addr_list.p", "rb" ) )
  return render_template("rest_name_render.html",name_and_addr_list=name_and_addr_list)#)
# CODE ACADEMY HTML CSS
@app.route('/mid_page', methods =['POST'])
def mid_page():
    #print request.form
    rest_name_and_addr = request.form['rest_name_and_addr']

    name_and_addr_list = pickle.load(open( "name_and_addr_list.p", "rb" ) )
    name_and_addr_idx = name_and_addr_list.index(rest_name_and_addr)

    name_and_addr_list_split = pickle.load(open( "name_and_addr_list_split.p", "rb" ) )
    all_menus = pd.read_pickle('all_menus.p')

    name_and_addr_split = name_and_addr_list_split[name_and_addr_idx]
    rest_name = name_and_addr_split[0]
    rest_address = name_and_addr_split[1]

    menu_item_list = all_menus[ (all_menus.restaurant_name ==  rest_name) & (all_menus.full_address ==  rest_address) ].item_name.tolist()
    #menu_item_list = [s.decode('utf-8') for s in menu_item_list]
    return render_template('menu_item_render.html',menu_item_list=menu_item_list,rest_name=rest_name,rest_address=rest_address)

@app.route('/result', methods =['POST'])
def result():

    rest_name = request.form['rest_name']
    rest_address = request.form['rest_address']
    menu_item = request.form['menu_item']

    all_menus = pd.read_pickle('all_menus.p')

    idx = all_menus[(all_menus.restaurant_name == rest_name) & (all_menus.full_address == rest_address) & (all_menus.item_name == menu_item)].index[0]
    tfidf_mat_menus = pickle.load(open( "tfidf_mat_menus.p", "rb" ) )

    user_selection, other_similar_items, menu_cosine_similarities = getTopMatches(tfidf_mat_menus,idx)

    num_sim_items = 5

    ctr = 0
    top_num_sim_items_list = []
    for cos_sim,sim_item in zip(menu_cosine_similarities,other_similar_items):
        if (all_menus.iloc[sim_item].name_and_address != all_menus.iloc[user_selection].name_and_address):
            top_num_sim_items_list.append(sim_item)
            ctr+=1
            if ctr == num_sim_items:
                break

    result_dict = []
    for i in top_num_sim_items_list:
        menu_print = all_menus.iloc[i].item_name
        desc_print = all_menus.iloc[i].item_description
        name_print = all_menus.iloc[i].restaurant_name
        price_print = all_menus.iloc[i].item_price
        address_print = all_menus.iloc[i].full_address
        yelp_rating_print = all_menus.iloc[i].yelp_rating
        yelp_link_print = all_menus.iloc[i].yelp_link
        result_dict.append(dict(menu_item=menu_print, desc=desc_print, name=name_print, price=price_print,address = address_print, yelp_rating = yelp_rating_print, yelp_link = yelp_link_print) )

    return render_template('result_render.html',rest_name=rest_name, menu_item=menu_item, result_dict = result_dict)

def getTopMatches(tfidf_mat,idx):

    # Compute the cosine similarity between the input idx and all the other vectors
    cosine_similarities = cosine_similarity(tfidf_mat[idx], tfidf_mat).flatten()

    # Organize the related food in descending order
    related_idcs = cosine_similarities.argsort()[::-1]

    # Organize the cosine similarities in descending order
    cosine_similarities_sorted = sorted(cosine_similarities, reverse=True)

    # Remove the user input
    user_selection = related_idcs[0]

    # The rest of them
    other_similar_items = related_idcs[1:]

    # Similarity metrics
    return user_selection,other_similar_items,cosine_similarities_sorted[1:]
