from bansheefixer.entities import *

class TableView(object):
    def __init__(self):
        self.columns = sorted([])

    def add_column(self, caption, function):
        self.columns.append((caption, function))

    def get_repr(self):
        s = self
        def f(iterable):
            rows = []

            # make the header captions
            rows.append([])
            for column in s.columns:
                rows[0].append(column[0])

            # loop through items and generate column strings
            lengths = [[] for column in s.columns]
            row_index = 0
            for item in iterable:
                row = []
                # loop through the columns and call the function ...
                column_index = 0
                item.__index__ = row_index
                for column in s.columns:
                    # run the function on the row to get a colunm
                    column_string = str(column[1](item))
                    row.append(column_string)
                    lengths[column_index].append(len(column_string))

                    column_index = column_index + 1

                rows.append(row)
                row_index = row_index + 1

            lengths_reduced = [max(length) for length in lengths]

            print(lengths_reduced)

            lines = []

            header = ["" for c in range(len(lengths_reduced))]

            rows.insert(1, header)
            for row in rows:
                padded_row = [str(row[c]).ljust(lengths_reduced[c]) for c in range(len(lengths_reduced))]
                line = "| " + " | ".join(padded_row) + " |"
                lines.append(line)

            return "\n".join(lines)

        return f

class Helper(object):
    def __init__(self, db):
        self.db = db

    def artist(self, name):
        return self.db.query(Artist).filter(Artist.Name.like(name))

    def album(self, title):
        return self.db.query(Album).filter(Album.Title.like(title))

    def track(self, title):
        return self.db.query(Track).filter(Track.Title.like(title))

class WorkingList(list):
    def __init__(self, tracklist):
        # Make a unique list of albums and artist in this track list
        self.artists = list(set([t.Artist for t in tracklist]))
        self.albums = list(set([t.Album for t in tracklist]))
        super().__init__(tracklist)

    def set_artist(self, artist):
        for t in self:
            t.Artist = artist

        self.artists = [artist]

        for a in self.albums:
            a.Artist = artist

        return self

    def set_year(self, year):
        for a in self.albums:
            a.Year = year

        for t in self:
            t.Year = year

    def set_album(self, album):
        self.albums = [album]

        for t in self:
            t.Album = album

    def sync_tags(self):
        for t in self:
            if t.Exists:
                t.write_tags()
            else:
                print(repr(t) + " NOT FOUND")

        print("You probably need to run 'session.commit()'")



