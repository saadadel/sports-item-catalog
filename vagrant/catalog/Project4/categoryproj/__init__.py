#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager(app)

from database import Base
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app.config['SECRET_KEY'] = \
    '5454d5as1d5asd4as5f1sd5c1sd6a8s7das6x4z3c1ds8c4sd'
bcrypt = Bcrypt(app)

login_manager.login_view = 'login'

from categoryproj import routes
