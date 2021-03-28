from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint

from .auth import login_required
from .models.gardener import Gardener
from .models.plant import plants
import html
import pandas as pd
import numpy as np
import sklearn as sklearn

bp = Blueprint('gardener', __name__)


@bp.route('/')
def index():
    ###Get plants from database##
    return render_template('gardener/index.html', plants=plants)


@ bp.route('/create', methods=('GET', 'POST'))
@ login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            ###Add plant to database
            return redirect(url_for('gardener.index'))

    return render_template('gardener/create.html')


#Modified code from Flask tutorial, but will need to get plant by id. SQL query needs to be evaluated, probably will
#use Pandas/NumPy/SkLearn here...


def get_plant(id, check_gardener=True):
    plant = get_db().execute(
        'SELECT p.id, gardener_id'
        ' FROM plant p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if plant is None:
        abort(404, "Plant id {0} doesn't exist.".format(id))

    if check_gardener and plant['gardener_id'] != g.user['id']:
        abort(403)

    return plant


@ bp.route('/<int:id>/update', methods=('GET', 'POST'))
@ login_required
def update(id):
    plant = get_plant(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('plant.index'))

    return render_template('plant/update.html', plant=plant)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_plant(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('plant.index'))


@bp.route('/search', methods=['GET', 'POST'])
def search_name():
    if request.method == 'POST':
        common_name = request.form['common_name']
        error = None
        search_results = []
        if not common_name:
            error = 'You must enter a name'
        for plant in plants:
            if common_name.upper() == plant.common_name.upper():
                error_common_name = False
                break
            else:
                error_common_name = True
        if error is not None:
            flash(error)
            return render_template('gardener/search.html', error=error)
        else:
            for plant in plants:
                if plant.common_name.upper() == common_name.upper():
                    common_name = plant.common_name
                    search_results.append(plant)

            return render_template('gardener/search_results.html', page_title=common_name, plant=search_results[0],
                                   plants=plants)
    else:
        return render_template('gardener/search.html')
