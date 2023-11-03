from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from . import db

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()
    return render_template('index.html', events=events)

@mainbp.route('/search')
def search():
    search_term = request.args.get('search', '')
    if search_term:
        print(search_term)
        query = f"%{search_term}%"
        events = db.session.scalars(db.select(Event).where(Event.description.like(query))).all()
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))
