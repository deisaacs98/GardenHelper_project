from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint
from .models.gardener import Gardener
from .models.plant import Plant
import html
import pandas as pd
import numpy as np
import sklearn as sklearn

bp = Blueprint('plant', __name__)




