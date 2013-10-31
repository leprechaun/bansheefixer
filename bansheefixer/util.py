from bansheefixer.entities import *

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

    def __repr__(self):
        lines = []

        lines.append("Artists:")
        for a in self.artists:
            lines.append("- #" + str(a.ArtistID) + " " + str(a.Name))

        lines.append("Albums:")
        for a in self.albums:
            lines.append("- #" + str(a.AlbumID) + " " + str(a.Title) + " (" + str(a.Year) + ")")

        lines.append("")

        artist_string_length = max([len(str(a.Name)) for a in self.artists])
        album_string_length = max([len(str(a.Title)) for a in self.albums])
        title_string_length = max([len(str(t.Title)) for t in self])
        track_string_length = len(str(len(self)))

        header = "+".ljust(track_string_length+3, "-") + "+".ljust(artist_string_length + 3, "-") + "+".ljust(album_string_length + 3, "-" ) + "+".ljust(title_string_length+6, "-") + "+"
        lines.append(header)
        i = 0
        for t in self:
            line = "| " + str(i).ljust(track_string_length+1) + "|"
            line = line + " " + str(t.Artist.Name).ljust(artist_string_length) + " |"
            line = line + " " + str(t.Album.Title).ljust(album_string_length) + " |"
            line = line + " " + str(t.TrackNumber).ljust(3) + str(t.Title).ljust(title_string_length+1) + "|"
            lines.append(line)
            i = i + 1

        lines.append(header)

        return "\n".join(lines)

    def sync_tags(self):
        for t in self:
            if t.Exists:
                t.write_tags()
            else:
                print(repr(t) + " NOT FOUND")

        print("You probably need to run 'session.commit()'")

