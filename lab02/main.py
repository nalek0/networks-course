import os
import json
import flask
from flask import Flask, request
from typing import Dict
from werkzeug.utils import secure_filename


class Product(object):
	"""Product class"""

	def __init__(self, product_id: int, name: str, description: str):
		self.icon = None;
		self.product_id = product_id
		self.name = name
		self.description = description

	def to_json(self):
		return {
			"id": 			self.product_id,
			"name": 		self.name,
			"icon": 		self.icon,
			"description": 	self.description,
		}


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
counter = 0
products: Dict[int, Product] = dict()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
	return "Index page"


@app.route("/product", methods=["POST"])
def product_post():
	global counter

	data = json.loads(request.data)
	name = data['name']
	description = data['description']
	product_id = counter
	counter += 1
	product = Product(product_id, name, description)
	products[product_id] = product

	return product.to_json()


@app.route("/product/<int:product_id>", methods=["GET", "PUT", "DELETE"])
def product_get(product_id: int):
	if request.method == "GET":
		if product_id in products.keys():
			product = products[product_id]

			return product.to_json();
		else:
			return "", 404
	elif request.method == "PUT":
		if product_id in products.keys():
			product = products[product_id]
			data = json.loads(request.data)

			if 'name' in data.keys():
				product.name = data['name']
			if 'description' in data.keys():
				product.description = data['description']
			
			return product.to_json();
		else:
			return "", 404
	elif request.method == "DELETE":
		if product_id in products.keys():
			product = products.pop(product_id)
			
			return product.to_json();
		else:
			return "", 404


@app.route("/products", methods=["GET"])
def product_list():
	result = []

	for product in products.values():
		result.append(product.to_json())
	
	return result


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/product/<int:product_id>/image", methods=["GET", "POST"])
def product_image(product_id: int):
	filename = secure_filename(f"icon#{product_id}.png")
	path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
	
	if request.method == "POST":
		if product_id not in products.keys():
			return "Product not found", 404
		
		product = products[product_id]

		# check if the post request has the file part
		if "icon" not in request.files:
			return "No icon found", 400
		
		file = request.files["icon"]
		
		# If the user does not select a file, the browser submits an
		# empty file without a filename.
		if file.filename == '':
			return "No selected file", 400
		elif file and allowed_file(file.filename):
			file.save(path)
			product.icon = f"/product/{product_id}/image"

			return ""
		else:
			return "File is not allowed", 400
	elif request.method == "GET":
		if product_id not in products.keys():
			return "Product not found", 404
		
		return flask.send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
	app.run(debug=True)
