from flask import Flask, request, render_template, flash, url_for, session as login_session
from categoryproj.database import Base, Category, Item, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()


if __name__ == '__main__':
  	first5 = session.query(Category).filter_by(id=[1,2,3,4,5])
