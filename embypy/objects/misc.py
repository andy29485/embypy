from embypy.objects.object import EmbyObject
from embypy.utils.asyncio import async_func


# Generic class
class Audio(EmbyObject):
    '''Class representing generic emby Audio objects

    Parameters
    ----------
      object_dict : dict
        same as for `EmbyObject`
      connector : embypy.utils.connector.Connector
        same as for `EmbyObject`
    '''
    def __init__(self, object_dict, connector):
        super().__init__(object_dict, connector)

    @property
    def album_id(self):
        '''the id of the album this song is in'''
        return self.object_dict.get('AlbumId')

    @property
    def album_name(self):
        '''name of album '''
        return self.object_dict.get('Album', '')

    @property
    @async_func
    async def album(self):
        '''The album that the song belongs to

        |coro|

        Returns
        -------
        :class:`embypy.objects.MusicAlbum`
        '''
        return await self.process(self.album_id)

    @property
    def index_number(self):
        '''track number on disc'''
        return self.object_dict.get('IndexNumber', 1)

    @index_number.setter
    def index_number(self, value):
        self.object_dict['IndexNumber'] = value

    @property
    def track_number(self):
        '''track number on disc'''
        return self.index_number

    @track_number.setter
    def track_number(self, value):
        self.index_number = value

    @property
    def album_artist_ids(self):
        '''list of album artist ids'''
        return [a['Id'] for a in self.object_dict.get('AlbumArtists', [])]

    @property
    def album_artist_names(self):
        '''names of album artists'''
        return self.object_dict.get('AlbumArtist', '').split(';')

    @property
    @async_func
    async def album_artists(self):
        '''

        |coro|

        Returns
        -------
        list
          of type :class:`embypy.objects.MusicArtist`
        '''
        return await self.process(self.album_artist_ids)

    @property
    def artist_ids(self):
        return [a['Id'] for a in self.object_dict.get('ArtistItems', [])]

    @property
    def artist_names(self):
        '''names of song artists'''
        return self.object_dict.get('Artists', [])

    @property
    @async_func
    async def artists(self):
        '''

        |coro|

        Returns
        -------
        list
          of type :class:`embypy.objects.MusicArtist`
        '''
        return await self.process(self.artist_ids)

    @property
    def album_primary_image_tag(self):
        '''The image tag of the album'''
        return self.object_dict.get('AlbumPrimaryImageTag')

    @property
    def album_primary_image_url(self):
        '''The image of the album'''
        path = '/Items/{}/Images/Primary'.format(self.album_id)
        return self.connector.get_url(path, attach_api_key=False)

    @property
    def media_type(self):
        return self.object_dict.get('MediaType', 'Audio')

    @property
    def type(self):
        return self.object_dict.get('Type', 'Audio')

    @property
    def stream_url(self):
        '''stream for this song - not re-encoded'''
        path = '/Audio/{}/universal'.format(self.id)
        return self.connector.get_url(
            path,
            userId=self.connector.userid,
            MaxStreamingBitrate=140000000,
            Container='opus',
            TranscodingContainer='opus',
            AudioCodec='opus',
            MaxSampleRate=48000,
            PlaySessionId=1496213367201  # TODO no hard code
        )


class Person(EmbyObject):
    '''Class representing emby people objects

    Parameters
    ----------
      object_dict : dict
        same as for `EmbyObject`
      connector : embypy.utils.connector.Connector
        same as for `EmbyObject`
    '''
    def __init__(self, object_dict, connector):
        super().__init__(object_dict, connector)

    @property
    def role(self):
        '''Role the person played as'''
        return self.object_dict.get('Role', '')

    @role.setter
    def role(self, value):
        self.object_dict['Role'] = value

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
    '''Class representing emby image objects

    Parameters
    ----------
      object_dict : dict
        same as for `EmbyObject`
      connector : embypy.utils.connector.Connector
        same as for `EmbyObject`
    '''
    def __init__(self, object_dict, connector):
        super().__init__(object_dict, connector)


# Game
class Game(EmbyObject):
    '''Class representing emby game objects

    Parameters
    ----------
      object_dict : dict
        same as for `EmbyObject`
      connector : embypy.utils.connector.Connector
        same as for `EmbyObject`
    '''
    def __init__(self, object_dict, connector):
        super().__init__(object_dict, connector)


class Photo(EmbyObject):
    '''Class representing emby photo objects

    Parameters
    ----------
      object_dict : dict
        same as for `EmbyObject`
      connector : embypy.utils.connector.Connector
        same as for `EmbyObject`
    '''
    def __init__(self, object_dict, connector):
        super().__init__(object_dict, connector)


#   Book
class Book(EmbyObject):
    '''Class representing emby book objects

    Parameters
    ----------
      object_dict : dict
        same as for `EmbyObject`
      connector : embypy.utils.connector.Connector
        same as for `EmbyObject`
    '''
    def __init__(self, object_dict, connector):
        super().__init__(object_dict, connector)


#   Device
class Device(EmbyObject):
    '''Class representing emby device objects

    Parameters
    ----------
      object_dict : dict
        same as for `EmbyObject`
      connector : embypy.utils.connector.Connector
        same as for `EmbyObject`
    '''
    def __init__(self, object_dict, connector):
        super().__init__(object_dict, connector)

    @property
    def last_user_name(self):
        return self.object_dict.get('LastUserName')

    @property
    def last_user_id(self):
        return self.object_dict.get('LastUserId')

    @property
    def app_name(self):
        return self.object_dict.get('AppName')

    @property
    def app_version(self):
        return self.object_dict.get('AppVersion')

    @property
    def date_last_activity(self):
        return self.object_dict.get('DateLastActivity')

    @property
    def icon_url(self):
        return self.object_dict.get('IconUrl')


class User(EmbyObject):
    '''Class representing emby user objects

    Parameters
    ----------
      object_dict : dict
        same as for `EmbyObject`
      connector : embypy.utils.connector.Connector
        same as for `EmbyObject`
    '''
    def __init__(self, object_dict, connector):
        super().__init__(object_dict, connector)

    @property
    def id(self):
        return self.object_dict.get('Id')

    @property
    def name(self):
        return self.object_dict.get('Name')

    @property
    def has_password(self):
        return self.object_dict.get('HasPassword')

    @property
    def has_configured_password(self):
        return self.object_dict.get('HasConfiguredPassword')

    @property
    def has__configured_easy_password(self):
        return self.object_dict.get('HasConfiguredEasyPassword')

    @property
    def configuration(self):
        return self.object_dict.get('Configuration')

    @property
    def policy(self):
        return self.object_dict.get('Policy')
