from flask import Flask, escape, request, render_template
import sys
import dbmgr
import sqlite3
import time
app = Flask(__name__)


def remove_empties(lst):
    return list(filter(lambda x: x != '', lst))

@app.route('/')
def hello():
    return render_template("index.html")

@app.route("/product_search.html")
def process_page():
   select_allergens = request.args.getlist("select_allergens")
   typed_allergens = request.args.get("ingredient_exclusions")

   search_terms = request.args.get("search_terms")
   lst_search_terms = search_terms.split(",")

   print(lst_search_terms)
   lst_all_allergens = typed_allergens.split(",") + select_allergens
   lst_all_allergens = remove_empties(lst_all_allergens)
   print(lst_all_allergens)
   query = dbmgr.construct_search_query(lst_all_allergens, lst_search_terms)
   
   conn = sqlite3.connect("Products.db")
   cursor = conn.cursor()
   entries = []
   print("entries scanning")
   print(query)
   for iterator in cursor.execute(query):
       entries.append(iterator)

   return render_template("products.html", entries=entries)
   
@app.route("/upc_match.html")
def product_and_image():
    upc = request.args.get("upc")
    if upc == None:
        return "No products found with that upc"
    conn = sqlite3.connect("Products.db")
    cursor = conn.cursor()
    entries = []
    print("Getting matching product: " + upc)
    query = "SELECT long_name, ingredients_english, gtin_upc from Products where gtin_upc = " + "'" + upc + "'"
    print("QUERY: " + query) 
    for iterator in cursor.execute(query):
        entries.append(iterator)
    
    # There should only be one entry
    entry = entries[0]
    return render_template("upc_match.html", entry=entry)
  
@app.route("/submit_product.html")
def route_product_page():
    return render_template("submit_product.html")

@app.route("/product_submission.html")
def route_product_submission():
    # Getting required fields for an entry
    upc = request.args.get("product_upc")
    name = request.args.get("product_name")
    manufacturer = request.args.get("product_manufacturer")
    ingredients = request.args.get("product_ingredients")
    default_source = "user:" + request.environ["REMOTE_ADDR"]
    
    
    date = time.strftime("%m/%d/%y %T")
    entry_tuple = (name, default_source, upc, manufacturer, date, date, ingredients)

    command = """INSERT INTO Experimental(long_name, data_source, gtin_upc, manufacturer, date_modified, date_available, ingredients_english)
                Values(?,?,?,?,?,?,?)"""
    
    connection = sqlite3.connect("Products.db")
    cur = connection.cursor()
    cur.execute(command, entry_tuple)
    connection.commit()
    connection.close()
    
    return str(cur.lastrowid)
    
    
if __name__ == "__main__":
    app.run(debug=True)
