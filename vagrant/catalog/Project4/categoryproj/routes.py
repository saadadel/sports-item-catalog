#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import request, render_template, flash, url_for, \
    session as login_session, flash, redirect, abort, jsonify
from categoryproj.database import Category, Item, User, Base
from categoryproj.forms import RegistrationForm, LoginForm, AddItem, \
    EditItem
from categoryproj import app, bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, logout_user, current_user, \
    login_required
from sqlalchemy import update, delete
import random
import string

# IMPORTS FOR G+ LOGIN
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

APPLICATION_NAME = 'Catalog Application'
# get the client id from the client secret file that was downloaded from G+ API
CLIENT_ID = json.loads(open('client_secrets.json', 'r')
                       .read())['web']['client_id']

# connect to the database
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# return items sorted according to the most new
def latestItems():
    items = session.query(Item).all()
    return list(reversed(items))


@app.errorhandler(403)
def user_not_authorized(e):
    flash("You don't have the permission to do this action")
    return redirect(url_for('main'))


# the main route
@app.route('/')
@app.route('/catalog')
def main():
    categories = session.query(Category).all()
    items = latestItems()
    return render_template(
        'main.html', categories=categories, items=items[:5], title='Main')


# route for specific category
@app.route('/catalog/<choosed_category>/items')
def categoryItemsList(choosed_category):
    cat = \
        session.query(Category).filter_by(name=choosed_category).one_or_none()
    items = session.query(Item).filter_by(category_id=cat.id)
    return render_template(
        'categoryItems.html', category=cat, items=items, title=cat.name)


# json endpoint for all cateogries and items
@app.route('/catalog.json')
def categoriesJSON():
    cats = session.query(Category).all()
    categoriesitems = []
    for cat in cats:
        items = session.query(Item).filter_by(category=cat)
        categoryitems = [cat.serialize, [item.serialize for item in items]]
        categoriesitems.append(categoryitems)
    return jsonify(category=categoriesitems)


# json endpoint for a specific cateogry
@app.route('/catalog.json/<category>')
def categoryJson(category):
    cat = session.query(Category).filter_by(name=category).one_or_none()
    items = session.query(Item).filter_by(category=cat).all()
    cat_json = [cat.serialize, [item.serialize for item in items]]
    return jsonify(caegory=cat_json)

# json endpoint for a specific item
@app.route('/catalog.json/<category>/<item>')
def itemJson(category, item):
    cat = session.query(Category).filter_by(name=category).one_or_none()
    item_obj = session.query(Item).filter_by(category=cat).filter_by(name=item).one_or_none()
    return jsonify(item = item_obj.serialize)


# add new item
@app.route('/additem', methods=['GET', 'POST'])
@login_required
def addItem():
    categories = session.query(Category).all()
    categories_names = []
    for category in categories:
        categories_names.append((category.name, category.name))
    form = AddItem()
    # fill the cateogreis list field
    form.category_name.choices = categories_names
    if form.validate_on_submit():
        choosed_category = \
            session.query(Category) \
            .filter_by(name=form.category_name.data).one_or_none()
        user = \
            session.query(User) \
            .filter_by(email=current_user.email).one_or_none()
        new_item = Item(
            name=form.item_name.data,
            description=form.description.data,
            category=choosed_category,
            user=user)
        session.add(new_item)
        session.commit()
        flash('Item Added Successfullysuccess')
        return redirect(url_for('main'))
    return render_template('add_item.html', title='Add_Item', form=form)


# route for a specific item in a specific category
@app.route('/catalog/<choosed_category>/<choosed_item>')
def categoryItems(choosed_category, choosed_item):
    cat = session.query(Category).filter_by(
        name=choosed_category).one_or_none()
    item = \
        session.query(Item). \
        filter_by(category=cat).filter_by(name=choosed_item).one_or_none()
    return render_template('itemDesc.html', item=item, title=choosed_item)


# edit an existing item
@app.route(
    '/catalog/<choosed_category>/<choosed_item>/edit',
    methods=['GET', 'POST'])
@login_required
def editItem(choosed_category, choosed_item):
    cat = session.query(Category).filter_by(
        name=choosed_category).one_or_none()
    item = \
        session.query(Item). \
        filter_by(category=cat).filter_by(name=choosed_item).one_or_none()
    form = EditItem(
        item_name=item.name, description=item.description
    )  # set a default values for the form fields
    if item.user.email != current_user.email:
        abort(403)
    if form.validate_on_submit():
        session.query(Item).filter_by(name=choosed_item).filter_by(
            category=item.category).update({
                'name': form.item_name.data,
                'description': form.description.data
            })
        session.commit()
        flash('Item Edited Successfully', 'success')
        return redirect(url_for('main'))
    return render_template(
        'edit_item.html', form=form, item=item, title='Edit_Item')


# delete an existing item
@app.route(
    '/catalog/<choosed_category>/<choosed_item>/delete',
    methods=['POST'])
@login_required
def deleteItem(choosed_category, choosed_item):
    cat = session.query(Category).filter_by(
        name=choosed_category).one_or_none()
    item = \
        session.query(Item). \
        filter_by(category=cat).filter_by(name=choosed_item).one_or_none()
    if item.user.email != current_user.email:
        abort(403)
    session.delete(item)
    session.commit()
    flash('Your item has been deleted!', 'success')
    return redirect(url_for('main'))


# Register to the App
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_passowrd = \
            bcrypt.generate_password_hash(form.password.data) \
            .decode('utf-8')
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_passowrd)
        session.add(new_user)
        session.commit()
        flash('Account created for {}!'.format(form.username.data), 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = \
            session.query(User).filter_by(email=form.email.data).one_or_none()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Logged in Successfully', 'success')
            return redirect(url_for('main'))
        else:
            flash('Login unsuccessful, Please check your email and password')
    return render_template('login.html', form=form, title="Login")


@app.route('/logout')
def logout():
    access_token = login_session.get('access_token')
    if access_token is not None:
        gdisconnect()
    logout_user()
    return redirect(url_for('main'))


# G+ login page
@app.route('/glogin')
def showGLogin():
    # Create anti-forgery state token
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in xrange(32))
    login_session['state'] = state
    return render_template('glogin.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():

    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = \
            make_response(json.dumps(
                'Failed to upgrade the authorization code.'),
                401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = \
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' \
        % access_token
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = \
            make_response(json.dumps(
                "Token's user ID doesn't match given user ID."),
                401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = \
            make_response(json.dumps(
                "Token's client ID does not match app's."),
                401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # make sure that the user is not already logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = \
            make_response(json.dumps(
                'Current user is already connected.'),
                200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += \
        ''' " style = "width: 300px; height: 300px;border-radius:
         150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''
    flash('you are now logged in as %s' % login_session['username'])
    print 'done!'

    # login the new user and create the account in the database if it's not
    new_user = session.query(User).filter_by(
        email=login_session['email']).one_or_none()
    if not new_user:
        new_user = User(
            username=login_session['username'],
            email=login_session['email'],
            password='googleaccount',
            image=login_session['picture'])
        session.add(new_user)
        session.commit()
    new_user = session.query(User).filter_by(
        email=login_session['email']).one_or_none()
    login_user(new_user)

    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = \
            make_response(json.dumps('Current user not connected.'),
                          401)
        response.headers['Content-Type'] = 'application/json'
        return response

    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        logout_user()
        return response
    else:
        response = \
            make_response(json.dumps(
                'Failed to revoke token for given user.',
                400))
        response.headers['Content-Type'] = 'application/json'
        return response
