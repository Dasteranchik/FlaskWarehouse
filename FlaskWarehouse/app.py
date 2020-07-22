"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///whouse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, unique=True, nullable=False)
	description = db.Column(db.Text(150))
	goods = db.relationship('Goods', backref='categor', lazy=True)

	def __repr__(self):
		return 'Category %r' % self.id


class Goods(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	category = db.Column(db.String, nullable=False)
	name = db.Column(db.String, unique=True, nullable=False)
	quantity = db.Column(db.Integer, nullable=False)
	description = db.Column(db.Text(150), nullable=False)
	price = db.Column(db.Float, nullable=False)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

	def __repr__(self):
		return 'Goods %r' % self.id


@app.route('/')
@app.route('/home')
@app.route('/category', methods=['POST','GET'])
def category():
	categorys = Category.query.order_by(Category.id).all()
	goods = Goods.query.order_by(Goods.id).all()
	return render_template(
		"category.html",
		categorys=categorys,
		goods=goods
		)

@app.route('/cat_create', methods = ['POST', 'GET'])
def cat_create():
	if request.method == "POST":
		name = request.form['name']
		description = request.form['description']
		category = Category(name=name, description=description)
		try:
			db.session.add(category)
			db.session.commit()
			return redirect('/category')
		except:
			return "Что-то не то"
	else:
		return render_template("cat_create.html")

@app.route('/category/<int:id>/cat_del')
def cat_del(id):
	category = Category.query.get_or_404(id)
	goods = Goods.query.filter(Goods.category_id.endswith(id)).all()
	try:
		db.session.delete(category)
		for el in goods:
			db.session.delete(el)
		db.session.commit()
		return redirect('/category')
	except:
		return "Что-то не то при удалении"

@app.route('/category/<int:id>/cat_edit', methods = ['POST', 'GET'])
def cat_edit(id):
	category = Category.query.get(id)
	if request.method == "POST":
		category.name = request.form['name']
		category.description = request.form['description']
		try:
			db.session.commit()
			return redirect('/category')
		except:
			return "Что-то не то"
	else:
		return render_template("cat_edit.html", category=category)

@app.route('/goods', methods=['POST','GET'])
def goods():
	categorys = Category.query.order_by(Category.id).all()
	goods = Goods.query.order_by(Goods.id).all()
	return render_template(
		"goods.html",
		goods=goods,
		categorys=categorys
		)

@app.route('/goods/<int:id>/goods', methods=['POST','GET'])
def g_cat(id):
	categorys = Category.query.order_by(Category.id).all()
	goods = Goods.query.filter(Goods.category_id.endswith(id)).all()
	return render_template(
		"goods.html",
		goods=goods,
		categorys=categorys,
		)

@app.route('/g_create', methods = ['POST', 'GET'])
def g_create():
	categorys = Category.query.order_by(Category.id).all()
	if request.method == "POST":
		category = request.form['category']
		name = request.form['name']
		quantity = request.form['quantity']
		description = request.form['description']
		price = request.form['price']
		for el in categorys:
			if (el.name == category):
				category_id = el.id
		goods = Goods(name=name, category=category, quantity=quantity, description=description, price=price, category_id=category_id)
		try:
			db.session.add(goods)
			db.session.commit()
			return redirect('/goods')
		except:
			return "Что-то не то"
	else:
		return render_template("g_create.html",
						 categorys=categorys
						 )

@app.route('/goods/<int:id>/g_del')
def g_del(id):
	goods = Goods.query.get_or_404(id)
	try:
		db.session.delete(goods)
		db.session.commit()
		return redirect('/goods')
	except:
		return "Что-то не то при удалении"

@app.route('/goods/<int:id>/g_edit', methods = ['POST', 'GET'])
def g_edit(id):
	categorys = Category.query.order_by(Category.id).all()
	goods = Goods.query.get(id)
	if request.method == "POST":
		goods.category = request.form['category']
		goods.name = request.form['name']
		goods.quantity = request.form['quantity']
		goods.description = request.form['description']
		goods.price = request.form['price']
		for el in categorys:
			if (el.name == category):
				goods.category_id = el.id
		try:
			db.session.commit()
			return redirect('/goods')
		except:
			return "Что-то не то"
	else:
		return render_template("g_edit.html",
						goods=goods,
						categorys=categorys)


if __name__ == '__main__':
	import os
	HOST = os.environ.get('SERVER_HOST', 'localhost')
	try:
		PORT = int(os.environ.get('SERVER_PORT', '5555'))
	except ValueError:
		PORT = 5555
	app.run(HOST, PORT)
