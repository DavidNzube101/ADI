# views.py

from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
import random
from flask_login import login_required, current_user
from sqlalchemy.sql import func  # Import the 'func' module
from .models import User
from . import db
import re
import datetime

# Implementations
from . import engine_implementation as ei

# My Modules
from . import DateSplitter as ds
from . import Gamble as gb

import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)


# Get the current date
current_date = datetime.date.today()

# Format the date as "YYYY-MM-DD"
formatted_date = current_date.strftime("%Y-%m-%d")

def ModelAnn(city, date):

    forecast = ei.BTLAnn(city=city, date=date)

    return forecast

def ModelLolo(city, date):
    results = ei.BTLLolo(city=city, date=date)
    
    forecast = results

    return forecast

def ModelCore(city, date):
    results = ei.BTLCore(city=city, date=date)
    
    forecast = results

    return forecast

def addCelcius(value):
    return f"{value}℃"


@views.route('/')
def home():
    return render_template("index.html")

@views.route('/apps')
def showAppsBoard():
    return render_template("apps.html")

@views.route('/football-predictor')
def footballPredictor():
    return render_template("Football-Index.html")

@views.route('/temperature-predictor', methods=['GET','POST'])
def temperaturePredictor():
    if request.method == 'POST':
        model = request.form['model']
        city = request.form['city']
        date = request.form['date'] # YYYY-MM-DD

        if model == 'Ann':
            results = ModelAnn(city=city, date=date)

        elif model == 'Lolo':
            results = ModelLolo(city=city, date=date)

        else:
            results = ModelCore(city=city, date=date)


        if gb.gamble([1, 2]) == 1:
            clean_date = ds.clean_date(formatted_date, style="MDY")
        else:
            clean_date = ds.clean_date(formatted_date)

        return render_template("Temp-index.html", weather=addCelcius(results), date=clean_date)
        # return render_template("Temp-index.html", date=clean_date)

    return render_template("Temp-index.html")# 