#!/usr/bin/env python3

import embypy.utils.connector

class EmbyObject:
  def __init__(self, object_dict, connector):
    self.connector   = connector
    self.object_dict = object_dict

  @property
  def id(self):
    return self.object_dict.get('Id') or self.object_dict.get('ItemId')

  @property
  def name(self):
    return self.object_dict.get('Name')

  @property
  def type(self):
    return self.object_dict.get('Type')

  @property
  def media_type(self):
    return self.object_dict.get('MediaType')

  @property
  def community_rating(self):
    return self.object_dict.get('CommunityRating')

  @property
  def primary_image_url(self):
    path = 'Items/{}/Images/Primary'.format(self.id)
    return self.connector.get_url(path)

  def update(self):
    path = 'Users/{}/Items/{}'.format(self.connector.userid, self.id)
    info = self.connector.getJson(path)
    self.object_dict.update(info)
    #return info

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

  def __str__(self):
    return self.name

  def __repr__(self):
    return '<{} {}>'.format(self.type, self.id)

# Generic classes
class Audio(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

  @property
  def album(self):
    return self.object_dict.get('Album')

  @property
  def album_artist(self):
    return self.object_dict.get('AlbumArtist')

  @property
  def artists(self):
    return self.object_dict.get('Artists')

  @property
  def album_id(self):
    return self.object_dict.get('AlbumId')

  @property
  def album_primary_image_tag(self):
    return self.object_dict.get('AlbumPrimaryImageTag')

  @property
  def media_type(self):
    return self.object_dict.get('MediaType')

  @property
  def type(self):
    return self.object_dict.get('Type')

  @property
  def index_number(self):
    return self.object_dict.get('IndexNumber')

  @property
  def genres(self):
    return self.object_dict.get('Genres')

  @property
  def tags(self):
    return self.object_dict.get('Tags')


class Video(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
  @property
  def aspect_ratio(self):
    return self.object_dict.get('AspectRatio')

  @property
  def chapters(self):
    return self.object_dict.get('Chapters')

  @property
  def overview(self):
    return self.object_dict.get('Overview')

  @property
  def genres(self):
    return self.object_dict.get('Genres')



class Folder(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
  @property
  def child_count(self):
    return self.object_dict.get('ChildCount')

  @property
  def cumulative_run_time(self):
    return self.object_dict.get('CumulativeRunTimeTicks')

  @property
  def genres(self):
    return self.object_dict.get('Genres')



class Person(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
  @property
  def name(self):
    return self.object_dict.get('Name')

  @property
  def role(self):
    return self.object_dict.get('Role')

  @property
  def type(self):
    return self.object_dict.get('Type')

  @property
  def primary_image_tag(self):
    return self.object_dict.get('PrimaryImageTag')

  @property
  def premiere_date(self):
    return self.object_dict.get('PremiereDate')


class Image(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)


# Videos
class Movie(Video):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
  @property
  def premiere_date(self):
    return self.object_dict.get('PremiereDate')


class Episode(Video):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
  @property
  def index_number(self):
    return self.object_dict.get('IndexNumber')

  @property
  def premiere_date(self):
    return self.object_dict.get('PremiereDate')

  @property
  def series_id(self):
    return self.object_dict.get('SeriesId')

  @property
  def series_name(self):
    return self.object_dict.get('SeriesName')

  @property
  def genres(self):
    return self.object_dict.get('SeriesGenres')

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

  @property
  def overview(self):
    return self.object_dict.get('Overview')

class MusicAlbum(Folder):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
  @property
  def album(self):
    return self.object_dict.get('Album')

  @property
  def album_artist(self):
    return self.object_dict.get('AlbumArtist')

  @property
  def artists(self):
    return self.object_dict.get('Artists')

  @property
  def album_id(self):
    return self.object_dict.get('AlbumId')

  @property
  def album_primary_image_tag(self):
    return self.object_dict.get('AlbumPrimaryImageTag')

  @property
  def premiere_date(self):
    return self.object_dict.get('PremiereDate')


class MusicArtist(Folder):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
  @property
  def premiere_date(self):
    return self.object_dict.get('PremiereDate')


class Season(Folder):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
  @property
  def index_number(self):
    return self.object_dict.get('IndexNumber')

  @property
  def played_percentage(self):
    return self.object_dict.get('PlayedPercentage')

  @property
  def overview(self):
    return self.object_dict.get('Overview')

  @property
  def series_id(self):
    return self.object_dict.get('SeriesId')

  @property
  def series_name(self):
    return self.object_dict.get('SeriesName')


class Series(Folder):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
  @property
  def air_days(self):
    return self.object_dict.get('AirDays')

  @property
  def air_time(self):
    return self.object_dict.get('AirTime')

  @property
  def status(self):
    return self.object_dict.get('Status')

  @property
  def premiere_date(self):
    return self.object_dict.get('PremiereDate')

  @property
  def overview(self):
    return self.object_dict.get('Overview')

  @property
  def season_count(self):
    return self.object_dict.get('SeasonCount')


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


