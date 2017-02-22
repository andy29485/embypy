#!/usr/bin/env python3

import embypy.utils.connector

class EmbyObject:
  def __init__(self, object_dict, connector):
    self.id               = object_dict.get('ItemId')
    self.name             = object_dict.get('Name')
    self.community_rating = object_dict.get('CommunityRating')
    self.connector        = connector

  def process(self, object_dict):
    if object_dict['Type'] == 'Audio':
      return Audio(object_dict, self.connector)
    if object_dict['Type'] == 'Person':
      return Person(object_dict, self.connector)
    if object_dict['Type'] == 'Video':
      return Series(object_dict, self.connector)
    if object_dict['Type'] == 'Movie':
      return Movie(object_dict, self.connector)
    if object_dict['Type'] == 'Trailer':
      return Trailer(object_dict, self.connector)
    if object_dict['Type'] == 'AdultVideo':
      return AdultVideo(object_dict, self.connector)
    if object_dict['Type'] == 'MusicVideo':
      return MusicVideo(object_dict, self.connector)
    if object_dict['Type'] == 'Episode':
      return Episode(object_dict, self.connector)
    if object_dict['Type'] == 'Folder':
      return Folder(object_dict, self.connector)
    if object_dict['Type'] == 'BoxSet':
      return BoxSet(object_dict, self.connector)
    if object_dict['Type'] == 'MusicAlbum':
      return MusicAlbum(object_dict, self.connector)
    if object_dict['Type'] == 'MusicArtist':
      return MusicArtist(object_dict, self.connector)
    if object_dict['Type'] == 'Season':
      return Season(object_dict, self.connector)
    if object_dict['Type'] == 'Series':
      return Series(object_dict, self.connector)
    if object_dict['Type'] == 'Game':
      return Game(object_dict, self.connector)
    if object_dict['Type'] == 'GameSystem':
      return GameSystem(object_dict, self.connector)
    if object_dict['Type'] == 'Photo':
      return Photo(object_dict, self.connector)
    if object_dict['Type'] == 'Book':
      return Book(object_dict, self.connector)
    if object_dict['Type'] == 'Image':
      return Image(object_dict, self.connector)

  def getPrimaryImageUrl(self):
    path = '/Items/' + self.id + '/Images/Primary'
    return urlunparse((self.connector.scheme,
                       self.connector.netloc, path,
                       '', '', ''
    ))

# Generic classes
class Audio(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
    self.album                   = object_dict.get('Album')
    self.album_artist            = object_dict.get('AlbumArtist')
    self.artists                 = object_dict.get('Artists')
    self.album_id                = object_dict.get('AlbumId')
    self.album_primary_image_tag = object_dict.get('AlbumPrimaryImageTag')
    self.media_type              = object_dict.get('MediaType')
    self.type                    = object_dict.get('Type')
    self.index_number            = object_dict.get('IndexNumber')
    self.genres                  = object_dict.get('Genres')
    self.tags                    = object_dict.get('Tags')

class Video(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
    self.aspect_ratio = object_dict.get('AspectRatio')
    self.chapters     = object_dict.get('Chapters')
    self.genres       = object_dict.get('Genres')


class Folder(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
    self.child_count         = object_dict.get('ChildCount')
    self.cumulative_run_time = object_dict.get('CumulativeRunTimeTicks')
    self.genres              = object_dict.get('Genres')


class Person(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
    self.name              = object_dict.get('Name')
    self.role              = object_dict.get('Role')
    self.type              = object_dict.get('Type')
    self.primary_image_tag = object_dict.get('PrimaryImageTag')
    self.premiere_date     = object_dict.get('PremiereDate')

class Image(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)


# Videos
class Movie(Video):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
    self.premiere_date = object_dict.get('PremiereDate')

class Episode(Video):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
    self.index_number  = object_dict.get('IndexNumber')
    self.premiere_date = object_dict.get('PremiereDate')
    self.series_id     = object_dict.get('SeriesId')
    self.series_name   = object_dict.get('SeriesName')

class Trailer(Video):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

class AdultVideo(Video):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

class MusicVideo(Video):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

# Folders
class BoxSet(Folder):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

class MusicAlbum(Folder):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
    self.album                   = object_dict.get('Album')
    self.album_artist            = object_dict.get('AlbumArtist')
    self.artists                 = object_dict.get('Artists')
    self.album_id                = object_dict.get('AlbumId')
    self.album_primary_image_tag = object_dict.get('AlbumPrimaryImageTag')
    self.premiere_date           = object_dict.get('PremiereDate')

class MusicArtist(Folder):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
    self.premiere_date = object_dict.get('PremiereDate')

class Season(Folder):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
    self.index_number      = object_dict.get('IndexNumber')
    self.played_percentage = object_dict.get('PlayedPercentage')
    self.series_id         = object_dict.get('SeriesId')
    self.series_name       = object_dict.get('SeriesName')

class Series(Folder):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
    self.air_days      = object_dict.get('AirDays')
    self.air_time      = object_dict.get('AirTime')
    self.status        = object_dict.get('Status')
    self.premiere_date = object_dict.get('PremiereDate')
    self.season_count  = object_dict.get('SeasonCount')

# Game
class Game(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

class GameSystem(Folder):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

# Book
class Book(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)


