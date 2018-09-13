from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flask import current_app, g
from flaskr.auth import login_required
from flaskr.db import get_db
from flask.cli import with_appcontext

import click

bp = Blueprint('crew', __name__, url_prefix="/crew")
def init_app(app):
    app.cli.add_command(init_crew_command)

def getCrew(id):
  db = get_db()
  crew = db.execute('SELECT c.*, s.id, s.name AS assignment_name FROM crew c LEFT JOIN station s ON c.assignment = s.id WHERE c.id = ?',(id,)).fetchone()
  return crew

@bp.route('/')
@login_required
def index():
  db = get_db()
  crew = db.execute('SELECT c.*, s.id, s.name AS assignment_name FROM crew c LEFT JOIN station s ON c.assignment = s.id').fetchall()
  return render_template('crew/index.html', crew=crew)

@bp.route('/<int:crew_id>')
@login_required
def single(crew_id):
  db = get_db()
  crew = getCrew(crew_id)
  stations = db.execute('SELECT id, name FROM station').fetchall()
  return render_template('crew/single.html', crew=crew, stations=stations)

@bp.route('/<int:crew_id>/assign', methods=['POST'])
@login_required
def assign(crew_id):
  crew = getCrew(crew_id)
  station = request.form['station']
  db = get_db()
  db.execute("UPDATE crew SET assignment = ? WHERE id = ?",(station, crew['id']))
  db.commit()
  flash("Crewmember assignment updated!")
  return render_template('crew/single.html', crew=crew)

@bp.route('/new', methods=('GET', 'POST'))
@login_required
def new():
  if request.method == 'POST':
      firstname = request.form['firstname']
      lastname  = request.form['lastname']
      rank      = request.form['rank']

      db = get_db()
      error = None

      if not firstname:
        error = "A first name is required"
      elif not lastname:
        error = "A last name is required"
      elif not rank:
        rank = "Assistant"
      elif db.execute("SELECT * FROM crew WHERE firstname = ? AND lastname = ?",(firstname, lastname,)).fetchone() is not None:
        error = "This crew member already exists"

      if error is None: 
        db.execute("INSERT INTO crew (firstname, lastname, rank) VALUES (?, ?, ?)", (firstname, lastname, rank,))
        db.commit()
        return redirect(url_for('crew.index'))

      flash(error)
  return render_template('crew/new.html')

def init_crew():
  db = get_db()
  with current_app.open_resource('sql/crew.sql') as f:
      db.executescript(f.read().decode('utf8'))

@click.command('init-crew')
@with_appcontext
def init_crew_command():
  """Add the crew table"""
  init_crew()
  click.echo('Crew table generated')