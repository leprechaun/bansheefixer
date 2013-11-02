#!/usr/bin/env python3

from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

from sqlalchemy import event

import logging
import stagger

import os.path

import urllib.parse

Base = declarative_base()

class Artist(Base):
    __tablename__ = "coreartists"

    ArtistID = Column(Integer, primary_key=True)
    TagSetID = Column(Integer)
    MusicBrainzID = Column(String)
    Name = Column(String)
    NameLowered = Column(String)
    NameSort = Column(String)
    NameSortKey = Column(String)
    Rating = Column(Integer)

    Albums = relationship("Album", backref="Artist", order_by="Album.Year")
    Tracks = relationship("Track", backref="Artist", order_by="Track.AlbumID")

    def __repr__(self):
        return "<Artist(#%s '%s')>" % (self.ArtistID, self.Name)

class Album(Base):
    __tablename__ = "corealbums"

    AlbumID = Column(Integer, primary_key=True)
    ArtistID = Column(Integer, ForeignKey("coreartists.ArtistID"))
    TagSetID = Column(Integer)

    MusicBrainzID = Column(String)

    Title = Column(String)
    TitleLowered = Column(String)
    TitleSort = Column(String)
    TitleSortKey = Column(String)

    ReleaseDate = Column(Integer)
    Duration = Column(Integer)
    Year = Column(Integer)
    IsCompilation = Column(Integer)

    ArtistName = Column(String)
    ArtistNameLowered = Column(String)
    ArtistNameSort = Column(String)
    ArtistNameSortKey = Column(String)

    Rating = Column(Integer)
    ArtworkID = Column(String)

    Tracks = relationship("Track", backref="Album")

    def __repr__(self):
        return "<Album(#%s '%s')>" % (self.AlbumID, self.Title)

class Track(Base):
    __tablename__ = "coretracks"

    PrimarySourceID = Column(Integer)
    TrackID = Column(Integer, primary_key=True)
    ArtistID = Column(Integer, ForeignKey("coreartists.ArtistID"))
    AlbumID = Column(Integer, ForeignKey("corealbums.AlbumID"))
    TagSetID = Column(Integer)
    ExternalID = Column(Integer)
    MusicBrainzID = Column(String)
    Uri = Column(String)
    MimeType = Column(String)
    FileSize = Column(Integer)
    BitRate = Column(String)
    SampleRate = Column(String)
    BitsPerSample = Column(String)
    Attributes = Column(Integer)
    LastStreamError = Column(Integer)

    @property
    def Location(self):
        return urllib.parse.unquote(self.Uri).replace("file://", "")

    @Location.setter
    def Location(self, location):
        self.Uri = "file://" + urllib.parse.quote(location)

    @property
    def Exists(self):
        return os.path.exists(self.Location)


    Title = Column(String)
    TitleLowered = Column(String)
    TitleSort = Column(String)
    TitleSortKey = Column(String)

    TrackNumber = Column(Integer)
    TrackCount = Column(Integer)
    Disc = Column(Integer)
    DiscCount = Column(Integer)

    Duration = Column(Integer)
    Year = Column(Integer)
    Genre = Column(String)
    Composer = Column(String)
    Conductor = Column(String)
    Grouping = Column(String)
    Copyright = Column(String)
    LicenseUri = Column(String)
    Comment = Column(String)
    Rating = Column(Integer)
    Score = Column(Integer)
    PlayCount = Column(Integer)
    SkipCount = Column(Integer)
    LastPlayedStamp = Column(Integer)
    LastSkippedStamp = Column(Integer)
    DateAddedStamp = Column(Integer)
    DateUpdatedStamp = Column(Integer)
    MetaDataHash = Column(String)
    BPM = Column(Integer)
    LastSyncedStamp = Column(Integer)
    FileModifiedStamp = Column(Integer)

    def write_tags(self):
        tags = stagger.read_tag(self.Location)

        tags.album = str(self.Album.Title)
        tags.album_artist = str(self.Album.ArtistName)
        tags.artist = str(self.Artist.Name)
        tags.comment = str(self.Comment)
        tags.composer = str(self.Composer)
        if self.Year != 0:
            tags.date = str(self.Year)
        tags.disc = str(self.Disc)
        tags.disc_total = str(self.DiscCount)
        tags.genre = str(self.Genre)
        tags.grouping = str(self.Grouping)
        tags.title = str(self.Title)
        tags.track = str(self.TrackNumber)
        tags.track_total = str(self.TrackCount)

        tags.write()

    def __repr__(self):
        return "<Track(#%s '%s' at '%s')>" % (self.TrackID, self.Title, self.Location)

@event.listens_for(Track.Title, "set")
def on_track_set_title(track, title, old_title, initiator):
    logging.info("Cascade Track.Title to Track.TitleLowered")
    track.TitleLowered = title.lower()

@event.listens_for(Album.Title, "set")
def on_track_set_title(album, title, old_title, initiator):
    album.TitleLowered = title.lower()

@event.listens_for(Album.ArtistID, "set")
def on_album_set_artist(album, artist_id, old_artist_id, initiator):
    album.ArtistName = album.Artist.Name

@event.listens_for(Album.ArtistName, "set")
def on_album_set_artist_name(album, artist_name, old_artist_name, initiator):
    album.ArtistNameLowered = artist_name.lower()
