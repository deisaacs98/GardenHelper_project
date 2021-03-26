from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint
from .models.gardener import Gardener
from .models.plant import plants
import html
import pandas as pd
import numpy as np
import sklearn as sklearn

bp = Blueprint('plant', __name__)


@bp.route('/Investment', methods=['GET'])


@bp.route('/Search',methods=['GET','POST'])
def SearchName():
    if request.method == 'POST':
        plant_common_name = request.form['common_name']
        error = None
        plants = []
        if not plant_common_name:
            error = 'You must enter a name'
        for plant in plants:
            if common_name.upper() == plant.common_name.upper():
                error_common_name = False
                break
            else:
                error_common_name = True
        if error_common_name == True:
            error = 'That game is not in the database'
        if error is not None:
            flash(error)
            return render_template('gardener/search.html', error=error)
        else:
            for plant in plants:
                if plant.common_name.upper() == common_name.upper():
                    common_name = plant.common_name
                    plants.append(plant)

            return render_template('gardener/search_results.html', page_title=plant_common_name, xs=xs, ys=ys,
                                           plant=plants[0], plants=plants)
    else:
        return render_template('gardener/search.html')

