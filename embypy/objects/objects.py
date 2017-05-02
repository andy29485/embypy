#!/usr/bin/env python3

import embypy.utils.connector
from .folders import *
from .videos import *
from .misc import *

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
    path = '/Items/{}/Images/Primary'.format(self.id)
    return self.connector.get_url(path)

  @property
  def url(self):
    path = '/web/itemdetails.html?id={}'.format(self.id)
    return self.connector.get_url(path)

  @property
  def parent_id(self):
    return self.object_dict.get('ParentId')

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
    return EmbyObject(object_dict, self.connector)

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

