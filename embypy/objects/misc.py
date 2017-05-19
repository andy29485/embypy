#!/usr/bin/env python3

from embypy.objects.object import *

# Generic class
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

  def stream(self):
    return self.connector.get_stream(self.stream_url)

  @property
  def stream_url(self):
    path = '/Audio/{}/stream.mp3'.format(self.id)
    return self.connector.get_url(path)


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


# Game
class Game(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

# Book
class Book(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
