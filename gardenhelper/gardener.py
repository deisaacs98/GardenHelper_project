from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint
from .models.gardener import Gardener
from .models.plant import plants
import html
import pandas as pd
import numpy as np
import sklearn as sklearn

bp = Blueprint('gardener', __name__)


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
