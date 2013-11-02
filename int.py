#!/usr/bin/env python3
"""Usage:
  int.py [--database=<database>]
"""

import sqlite3
import urllib
from urllib import parse
import stagger
from docopt import docopt
import os.path

from bansheefixer.entities import *
from bansheefixer.util import *
from bansheefixer.fixes import *

arguments = docopt(__doc__, version='0.1.1rc')
if arguments['--database'] is not None:
    path = os.path.expanduser(arguments['--database'])
else:
    path = os.path.expanduser("~/.config/banshee-1/banshee.db")

engine = create_engine('sqlite:///' + path)


Session = sessionmaker(bind=engine)
session = Session()

#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

q = session.query
h = Helper(session)

tv = TableView()
tv.add_column("#", lambda t: str(t.__index__))
tv.add_column("ID", lambda t: str(t.TrackID))
tv.add_column("Artist", lambda t: str(t.Artist.Name) + " (#" + str(t.Artist.ArtistID)+")")
tv.add_column("Album", lambda t: str(t.Album.Title) + " (#" + str(t.Album.AlbumID)+")")
tv.add_column("T#", lambda t: "#" + str(t.TrackNumber) + "/" + str(t.TrackCount))
tv.add_column("Title", lambda t: str(t.Title))

WorkingList.__repr__ = tv.get_repr()


def commit():
    session.commit()
    wl.sync_tags()
