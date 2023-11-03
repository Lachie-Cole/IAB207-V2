from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

eventbp = Blueprint('event', __name__, url_prefix='/events')

@eventbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    # create the comment form
    form = CommentForm()
    return render_template('events/show.html', event=event, form=form)

@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = EventForm()
    if form.validate_on_submit():
        db_file_path = check_upload_file(form)
        event = Event(
            user_id=current_user.id,
            title=form.title.data,
            genre=form.genre.data,
            artist_or_band=form.artist_or_band.data,
            location=form.location.data,
            event_date=form.event_date.data,
            description=form.description.data,
            tickets_available=form.tickets_available.data,
            image_path=db_file_path,
        )
        db.session.add(event)
        db.session.commit()
        flash('Successfully created new event', 'success')
        return redirect(url_for('event.show', id=event.id))
    return render_template('events/create.html', form=form)

def check_upload_file(form):
    fp = form.image.data
    filename = fp.filename
    BASE_PATH = os.path.dirname(__file__)
    upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
    db_upload_path = 'image/' + secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path

@eventbp.route('/<id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if form.validate_on_submit():
        comment = Comment(text=form.text.data, event_id=event.id, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added to the event', 'success')
    return redirect(url_for('event.show', id=id))
