#!/bin/env python3
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response

import config
from src.app import app
from .permission_handler import PermissionHandler
from src.util.apperror import AppError

main = Blueprint('main', __name__)

@app.route('/')
def index():
    if 'login' not in session: return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            db = config.get_database()
            user = db.select1('Users', Login=request.form['login'])
            if user:
                session['login'] = user.Login
                session['name'] = user.Name
                session['prod_month'] = user.ProdMonth
                session['permissions'] = user.Permissions
                return redirect(url_for('index'))
            else:
                return "User not found"
        except:
            flash("No such user was found in the system.")
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('index')))
    if 'login' in session:
        session.clear()
        resp.set_cookie('proddate', expires=0)
    return resp
    # return redirect(url_for('index'))

@app.route('/map')
def map():
    import random, json
    db = config.get_database()
    statement_wellevents = "SELECT * FROM WellEventInfo LIMIT 5"
    wellevents = db.select_sql(statement_wellevents)

    results = []
    for wellevent in wellevents:
        json_obj = {}
        json_obj['type'] = 'Feature'
        json_obj['properties'] = {}
        json_obj['properties']['name'] = wellevent.WellEvent
        json_obj['properties']['popupContent'] = '<b>%s</b> <br> Pool Name: %s<br><a href="/wellevent/%s">Details</a>' % (wellevent.WellEvent, wellevent.PoolName, wellevent.WellEvent)
        json_obj['geometry'] = {}
        json_obj['geometry']['type'] = 'Point'
        json_obj['geometry']['coordinates'] = [random.randint(1, 50), random.randint(1, 100)]
        results.append(json_obj)
    print(results)
    return render_template('map.html', results=json.dumps(results))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')

def get_proddate():
    cookie = request.cookies['proddate']
    if not cookie: raise AppError('Proddate cookie not set for some reason')
    proddate = cookie[0:4] + "-" + cookie[4:6] + "-01"
    return proddate

def get_proddate_int():
    try:
        return int(request.cookies['proddate'])
    except:
        raise AppError('Proddate cookie not set for some reason')

"""
V 1. Authentication system
    V a. Checkboxes for permissions (names like well_edit, on server added to a list if checked, then list = permissions in db)
    V b. JS-based form verification before submitting (use jQuery dialog demo for example)
    V c. If permissions not set, default them to Disabled
2. Well event view
    a. Search by well event only
    b. Search results based on Lorraine's table
    c. Details page - show entire record
    d. Details page - show related wells
    e. Search fields verification; get rid of empty fields in JS
3. Lease view
    V a. Start by designing url structure!
    b. No search for now
    c. Search results - show entire record
    d. Details page - show entire record
    e. Details page - show related wells
3. Larry's data view
    a. Make sure it's working
4. Production month
    a. Store in cookies, make sure persistent for user on this computer
    b. Prompt a user if it's not set
    c. Write a function that would get it consistently
5. Misc
    a. Implement flash messages (how to make it work from JS?)
    b. Change all endpoints to make use of GET parameters: /lease/search?ID=1&Prov=AB, then populate the form if these were passed on:
       value = {{ lease.ID or "" }}

Questions to Larry:
1. select_sql when expecting just one result? if result.len==1 return result[0]?
2. No leases in Lease table matching the WellLeaseLink lookup results
3. Almost no results when taking into account production date.

1. Try outer joins for dates to have fields empty where date doesn't match
2. If available, include results from Well in WellEvent details
3. Change the Facility details view to a separate page a-lá WellEvent
4. Change the proddate modal to update text instantly

Idea: change all db.select functions to take into account the production date (to avoid setting it manually on every query)
"""
