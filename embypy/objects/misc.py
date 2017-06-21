#!/usr/bin/env python3

from embypy.objects.object import *

# Generic class
class Audio(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)

  @property
  def album_id(self):
    return self.object_dict.get('AlbumId')

  @property
  def album(self):
    return self.process(self.album_id)

  @property
  def index_number(self):
    return self.object_dict.get('IndexNumber')

  @property
  def track_number(self):
    return self.index_number

  @property
  def album_artist_ids(self):
    return [a['Id'] for a in self.object_dict.get('AlbumArtists', [])]

  @property
  def album_artist_name(self):
    return self.object_dict.get('AlbumArtist', [])

  @property
  def album_artists(self):
    return self.process(self.album_artist_ids)

  @property
  def artist_ids(self):
    return [a['Id'] for a in self.object_dict.get('ArtistItems', [])]

  @property
  def artist_names(self):
    return self.object_dict.get('Artists', [])

  @property
  def artists(self):
    return self.process(self.artist_ids)

  @property
  def album_primary_image_tag(self):
    return self.object_dict.get('AlbumPrimaryImageTag')

  @property
  def media_type(self):
    return self.object_dict.get('MediaType', 'Audio')

  @property
  def type(self):
    return self.object_dict.get('Type', 'Audio')

  @property
  def index_number(self):
    return self.object_dict.get('IndexNumber', 0)

  @property
  def genres(self):
    return self.object_dict.get('Genres', [])

  @property
  def tags(self):
    return self.object_dict.get('Tags', [])

  def stream(self):
    return self.connector.get_stream(self.stream_url)

  @property
  def stream_url(self):
    path = '/Audio/{}/universal'.format(self.id)
    return self.connector.get_url(path,
                                  userId=self.connector.userid,
                                  MaxStreamingBitrate=140000000,
                                  Container='opus',
                                  TranscodingContainer='opus',
                                  AudioCodec='opus',
                                  MaxSampleRate=48000,
                                  PlaySessionId=1496213367201 #TODO no hard code
    )


class Person(EmbyObject):
  def __init__(self, object_dict, connector):
    super().__init__(object_dict, connector)
  @property
  def name(self):
    return self.object_dict.get('Name', '')

  @property
  def role(self):
    return self.object_dict.get('Role', '')

  @property
  def type(self):
    return self.object_dict.get('Type', 'Person')

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
