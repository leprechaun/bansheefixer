#!/usr/bin/env python3

import sqlite3
import urllib
from urllib import parse
import stagger

import os.path

from entities import *
from util import *


engine = create_engine('sqlite:////home/leprechaun/.config/banshee-1/banshee.db')
Session = sessionmaker(bind=engine)
session = Session()

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

q = session.query
h = Helper(session)
