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

will write the tags to all files in the WorkingList, provided they are found.



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

