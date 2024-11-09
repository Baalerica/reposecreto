from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'secret_key'

uri = 'uri = 'mongodb+srv://estradaf809:gmRuDE6tWCmf2B7A@cluster0.8tkxz.mongodb.net/jalawei?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['inventario']
productos_collection = db['productos']

@app.route('/')
def index():
    productos = list(productos_collection.find())
    return render_template('index.html', productos=productos)

@app.route('/add_to_cart/<product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    flash('Producto agregado al carrito!', 'success')
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart_items = []
    if 'cart' in session:
        # Convertir los IDs de productos en ObjectId para la consulta en MongoDB
        product_ids = [ObjectId(id) for id in session['cart']]
        cart_items = list(productos_collection.find({'_id': {'$in': product_ids}}))
    return render_template('cart.html', cart_items=cart_items)

@app.route('/remove_from_cart/<product_id>')
def remove_from_cart(product_id):
    if 'cart' in session and product_id in session['cart']:
        session['cart'].remove(product_id)
        flash('Producto eliminado del carrito', 'info')
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)