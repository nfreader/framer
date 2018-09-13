#!/usr/bin/env python
import os
from flask import Flask
from . import db, auth, crew, station

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
	)

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	# a simple page that says hello
	@app.route('/hello')
	def hello():
		return 'Hello, World!'

	db.init_app(app)
	station.init_app(app)
	crew.init_app(app)
	app.register_blueprint(auth.bp)
	app.register_blueprint(station.bp)
	app.register_blueprint(crew.bp)

	return app