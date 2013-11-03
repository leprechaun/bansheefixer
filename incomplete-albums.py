#!/usr/bin/env python3
"""Usage:
  scanner3.py [--database=<database>]
"""

from bansheefixer.entities import *
from bansheefixer.util import *
from bansheefixer.fixes import *
from docopt import docopt
import re

from sqlalchemy import distinct

tv = TableView()
tv.add_column("#", lambda t: str(t.__index__))
tv.add_column("ID", lambda t: str(t.TrackID))
tv.add_column("Artist", lambda t: str(t.Artist.Name) + " (#" + str(t.Artist.ArtistID)+")")
tv.add_column("Album", lambda t: str(t.Album.Title) + " (#" + str(t.Album.AlbumID)+")")
tv.add_column("T#", lambda t: "#" + str(t.TrackNumber) + "/" + str(t.TrackCount))
tv.add_column("Title", lambda t: str(t.Title))
tv.add_column("OK", lambda t: str(t.Exists))

WorkingList.__repr__ = tv.get_repr()



if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1.1rc')

    if arguments['--database'] is not None:
        path = os.path.expanduser(arguments['--database'])
    else:
        path = os.path.expanduser("~/.config/banshee-1/banshee.db")

    engine = create_engine('sqlite:///' + path)
    Session = sessionmaker(bind=engine)
    session = Session()


    h = Helper(session)


    def looper():
        # Compilations are a bit tricky right now
        # Many have multiple Album entries for each artist
        # they can live another day
        albums = session.query(Album).filter_by(IsCompilation=0)

        distinct_album_titles = session.query(distinct(Album.Title)).all()

        for album_title in distinct_album_titles:
            # because this is a tuple to begin with
            album_title = album_title[0]

            all_tracks = []
            search = session.query(Album).filter_by(Title=album_title).all()

            [all_tracks.extend(s.Tracks) for s in search]

            tracks = all_tracks

            for t in tracks:
                if t.Exists is not True:
                    tracks.remove(t)

            if len(tracks) == 0:
                continue


            track_numbers = [t.TrackNumber for t in tracks]
            track_counts = [t.TrackCount for t in tracks]
            disc_numbers = [t.Disc for t in tracks]
            disc_counts = [t.DiscCount for t in tracks]

            track_numbers.sort()
            track_counts.sort()
            disc_numbers.sort()
            disc_counts.sort()

            artists = list(set([t.Artist for t in tracks]))

            artist_to_tracks_ratio = round((len(tracks) / len(artists)) / len(tracks), 2)

            sorter = [(t.TrackNumber, t.Title, t.TrackID, t) for t in tracks]
            sorter.sort()
            tracks = [t[3] for t in sorter]


            has_less_tracks_than_max_track_number = max(track_numbers) > len(tracks)

            likely_incomplete = False

            if has_less_tracks_than_max_track_number:
                likely_incomplete = True

            if likely_incomplete:
                wl = WorkingList(tracks)

                print("Likely problematic")
                print(track_numbers)
                print(track_counts)
                print()
                print(disc_numbers)
                print(disc_counts)
                print(wl)
                print()
                print("Track/Artist ratio:", str(artist_to_tracks_ratio))
                print()


                yield wl
