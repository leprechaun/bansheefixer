#!/usr/bin/env python
"""Usage:
  file-presence.py [--database=<database>]
"""

from bansheefixer.entities import *
from bansheefixer.util import *
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1.1rc')

    if arguments['--database'] is not None:
        path = os.path.expanduser(arguments['--database'])
    else:
        path = os.path.expanduser("~/.config/banshee-1/banshee.db")

    engine = create_engine('sqlite:///' + path)
    Session = sessionmaker(bind=engine)
    session = Session()

    tracks = session.query(Track).all()

    for t in tracks:
        if t.Exists == False:
            print("NOT FOUND: " + str(t.TrackID) + "\t" + t.Location)
