from flask import render_template, redirect, url_for, Blueprint, request
from string import ascii_letters, digits
from random import choice
from . import db
from .models import NewURL

views = Blueprint("views", __name__)

@views.route('/', methods=['GET', 'POST'])
def shorten_url():
    if request.method == 'POST':
        url = request.form.get('url')
        short_url = ''.join(choice(ascii_letters + digits) for i in range(8))

        shortened = NewURL(original=url, short=short_url)
        db.session.add(shortened)
        db.session.commit()
        new_url = request.host_url + short_url
        return render_template('index.html', new=new_url)

    return render_template('index.html')

@views.route('/<short>')
def redirect_short(short):
    link = NewURL.query.filter_by(short=short).first()
    if link:
        return redirect(link.original)
    else:
        return redirect(url_for('views.shorten_url'))