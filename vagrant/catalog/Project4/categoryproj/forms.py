#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, \
    BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
    ValidationError
from categoryproj.database import User, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class RegistrationForm(FlaskForm):

    username = StringField(
        'Username', validators=[DataRequired(),
                                Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(),
                                        EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = session.query(User).filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email already have an account.')


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remeber Me')
    submit = SubmitField('Login')


class AddItem(FlaskForm):
    """docstring for AddItem"""

    category_name = SelectField('Categroy Name', validators=[DataRequired()])
    item_name = StringField('Item Name', validators=[DataRequired()])
    description = StringField('Decription', validators=[DataRequired()])

    submit = SubmitField('Apply')


class EditItem(FlaskForm):
    """docstring for AddItem"""

    item_name = StringField('Item Name', validators=[DataRequired()])
    description = TextAreaField('Decription', validators=[DataRequired()])

    submit = SubmitField('Apply')
