BansheeFixer
=============

BansheeFixer is meant to be a small Python 3 DSL based on SQLAlchemy that allows for fixing of ID3 tags and Banshee's sqlite metadata. ID3 data is handled by the stagger library.


Entities
--------

* Artist
Has Albums and Tracks as relationships and provides the appropriate backrefs

* Album
Has the Artist backref and a Tracks collection

* Track
Has Artist and Album backrefs. See also Track.Location (translates Track.Uri), Track.Exits (check file presence)


Running
-------
You can run BansheeFixer by running python in interactive mode.

    python3 -i int.py [--database=path_to_your_banshee_data]



Helper aka h
------------

You can easily query artists, albums or tracks by using the *h* helper.

    h.artist('jamiroquai')
    h.album('travelling without moving')
    h.track('travelling without moving')

Any of those methods will return a *sqlalchemy.orm.query.Query* object. Therefore you must

    h.artist('jamiroquai').all()
    h.artist('jamiroquai').first()

The matching is, for now, simply done on the "NameLowered" or "TitleLowered" of the given entities.


WorkingList
-----------

WorkingList extends Python's <list> basic type and is made to contain Track objects. It offers a few helpful functions:

    wl = WorkingList(h.artist('jamiroquai').first().Tracks)

Working list provides a few helper methods

    wl.set_artist(artist_entity)

will set Artist on all tracks as well as albums in the Working list

    wl.set_album(album_entity)
    wl.set_year(year)

Will do what you think they do.

    wl.sync_tags()

You should run session.commit() to write the changes to the database. The script could crash if you keep banshee running while doing this, but more often than not, it does not. The WorkingList in banshee will refresh next time you play one of its items.

will write the tags to all files in the WorkingList, provided they are found.

WorkingList.__repr__ is meant to be human readable, as such:

    >>> wl
    Artists:
    - #1209 Jamiroquai
    Albums:
    - #1845 Emergency On Planet Earth (None)

    +----+------------+---------------------------+--------------------------------------+
    | 0  | Jamiroquai | Emergency On Planet Earth | 1  When You Gonna Learn (Digerido    |
    | 1  | Jamiroquai | Emergency On Planet Earth | 2  Too Young To Die                  |
    | 2  | Jamiroquai | Emergency On Planet Earth | 3  Hooked Up                         |
    | 3  | Jamiroquai | Emergency On Planet Earth | 4  If I Like It, I Do It             |
    | 4  | Jamiroquai | Emergency On Planet Earth | 5  Music Of The Mind                 |
    | 5  | Jamiroquai | Emergency On Planet Earth | 6  Emergency On Planet Earth         |
    | 6  | Jamiroquai | Emergency On Planet Earth | 7  Whatever It Is, I Just Can't Stop |
    | 7  | Jamiroquai | Emergency On Planet Earth | 8  Blow Your Mind                    |
    | 8  | Jamiroquai | Emergency On Planet Earth | 9  Revolution 1993                   |
    | 9  | Jamiroquai | Emergency On Planet Earth | 10 Didgin' Out                       |
    +----+------------+---------------------------+--------------------------------------+

List indexes are given on the left so you can easily do slicing, eg

    new_wl = WorkingList(wl[1:])



Fixes
-----
The fixes module include common fixes I've needed on my collection

    # TrackNumberInTitle takes care of albums with titles like
    # "01 - The Return Of The Space Cowboy"
    # It will .split() Track.Title, set Track.TrackNumber and Track.Title appropriately
    f = TrackNumberInTitle(" - ")
    f.apply(wl)

    # StripFromTitle will run Track.Title.lstrip()
    f = StripFromTitle("Jamiroquai - ")
    f.apply(wl)


Other files
-----------
file-presence.py is an example script that checks for files that don't exist in your library. There may be a bug as I suspect the inplementation of urllib.parse.unquote is not the same as the one in banshee (big surprise).



Current problems
----------------
I haven't managed to get SQLAlchemy events working completely. Look at entities.py,
when you update Track.Title, it should also update Track.TitleLowered appropriately.
However, I haven't managed to get events working on the backrefs, eg, change the artist on a track. This may be a source of issues because the banshee database does a bit of denormalization. Nothing that will delete or otherwise irreperably harm your library, though (fingers crossed).
