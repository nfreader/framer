from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flask import current_app, g
from flaskr.auth import login_required
from flask.cli import with_appcontext
from flaskr.db import get_db

import functools
import click
import os
import secrets

bp = Blueprint('station', __name__, url_prefix="/stations")
def init_app(app):
    app.cli.add_command(gen_stations_command)
    app.cli.add_command(init_stations_command)

@bp.route('/')
@login_required
def getStations():
	db = get_db()
	stations = db.execute('SELECT s.id, s.name, COUNT(c.id) AS crew FROM station s LEFT JOIN crew c ON s.id = c.assignment GROUP BY s.id').fetchall()
	return render_template('stations/listing.html', stations=stations)

@bp.route('/<int:station_id>')
@login_required
def view(station_id):
	db = get_db()
	station = db.execute('SELECT s.id, s.name, COUNT(c.id) AS crew FROM station s LEFT JOIN crew c ON s.id = c.assignment WHERE s.id = ? GROUP BY s.id', (station_id,)).fetchone()
	return render_template('stations/single.html', station=station)

def init_stations():
	db = get_db()
	with current_app.open_resource('sql/station.sql') as f:
	    db.executescript(f.read().decode('utf8'))

@click.command('init-stations')
@with_appcontext
def init_stations_command():
	"""Add the stations table"""
	init_stations()
	click.echo('Station table generated')

def gen_stations():
	f = open('flaskr/static/names/station/name.txt','r')
	names = f.read().split("\n")
	print(names)
	f.close()

	f = open('flaskr/static/names/station/prefix.txt','r')
	prefix = f.read().split("\n")
	print(prefix)
	f.close()

	f = open('flaskr/static/names/station/suffix.txt','r')
	suffix = f.read().split("\n")
	print(suffix)
	f.close()

	db = get_db()
	count = 0
	while (count < 10):
		finalName = "{0} {1} {2}".format(secrets.choice(prefix), secrets.choice(names), secrets.choice(suffix))

		db.execute(
			'INSERT INTO station (name) VALUES (?)', (finalName,)
		)
		db.commit()
		count = count + 1
	return

@click.command('generate-stations')
@with_appcontext
def gen_stations_command():
	"""Generate some space stations"""
	gen_stations()
	click.echo('Generated some stations')