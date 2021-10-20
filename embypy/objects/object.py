from embypy.utils.asyncio import async_func

import arrow
import datetime

_EMPTY_OBJ = {
    "Id": "",
    "Name": "",
    "OriginalTitle": "",
    "ForcedSortName": "",
    "CommunityRating": "",
    "CriticRating": "",
    "IndexNumber": "",
    "AirsBeforeSeasonNumber": "",
    "AirsAfterSeasonNumber": "",
    "AirsBeforeEpisodeNumber": "",
    "ParentIndexNumber": None,
    "DisplayOrder": "",
    "Album": "",
    "AlbumArtists": [],
    "ArtistItems": [],
    "Overview": "",
    "Status": "",
    "AirDays": [],
    "AirTime": "",
    "Genres": [],
    "Tags": [],
    "Studios": [],
    "PremiereDate": "",
    "DateCreated": "",
    "EndDate": None,
    "ProductionYear": "",
    "AspectRatio": "",
    "Video3DFormat": "",
    "OfficialRating": "",
    "CustomRating": "",
    "People": [],
    "LockData": False,
    "LockedFields": [],
    "ProviderIds": {
        "MusicBrainzReleaseGroup": "",
        "MusicBrainzAlbumArtist": "",
        "MusicBrainzAlbum": "",
        "MusicBrainzArtist": "",
        "MusicBrainzTrack": "",
        "AudioDbAlbum": "",
        "AudioDbArtist": ""
    },
    "PreferredMetadataLanguage": "",
    "PreferredMetadataCountryCode": "",
    "Taglines": []
}


class EmbyObject(object):
    '''Deafult EMby Object Template

    Parameters
    ----------
    object_dict : dict
      dictionary with json info returned from emby
    connector: embypy.utils.connector.Connector
      connector object to make upstream api calls
    save : bool
      if true, append to list of existing objects
      saves space/increases speed/reduces issues
      only set to false if creating a temp object that will be thrown out
    '''
    known_objects = {}

    def __init__(self, object_dict, connector, save=True):
        self.connector = connector
        self.object_dict = object_dict
        self.extras = {}
        if save:
            EmbyObject.known_objects[object_dict.get('Id')] = self

    def __eq__(self, other):
        return isinstance(other, EmbyObject) and self.id == other.id

    def __setattr__(self, name, value):
        if name.endswith('_sync'):
            return self.__setattr__(name[:-5], value)
        super().__setattr__(name, value)

    def __getattr__(self, name):
        if name.endswith('_sync'):
            return self.__getattr__(name[:-5])
        return self.__getattribute__(name)

    @property
    def id(self):
        '''string with hexidecimal hash representing the id of this
        object in emby
        '''
        return self.object_dict.get('Id') or self.object_dict.get('ItemId')

    @property
    def name(self):
        '''name of the item

        See Also
        --------
          post :
        '''
        return self.object_dict.get('Name', '')

    @name.setter
    def name(self, value):
        self.object_dict['Name'] = value

    @property
    def title(self):
        '''same as name

        See Also
        --------
          post :
        '''
        return self.name

    @title.setter
    def title(self, value):
        self.name = value

    @property
    def path(self):
        '''get the filepath of the media file (not url)

        See Also
        --------
          url :
        '''
        return self.object_dict.get('Path', '')

    @property
    def watched(self):
        '''returns True it item has been watched'''
        return self.object_dict.get('UserData', {}).get('Played')

    @property
    def played(self):
        '''same as `watched`'''
        return self.watched

    @property
    def percentage_played(self):
        '''returns played percentage [0,1] of item'''
        played = self.object_dict.get(
            'UserData', {}
        ).get('PlaybackPositionTicks')
        total = self.object_dict.get('RunTimeTicks') or played or 1
        return (played or 0) / total

    @property
    def duration(self):
        '''returns duration of item in seconds'''
        return self.object_dict.get('RunTimeTicks', 0) / (10**7)

    @property
    def play_count(self):
        '''returns users playcount for item'''
        return self.object_dict.get('UserData', {}).get('PlayCount', 0)

    @property
    def favorite(self):
        '''returns True if user favorited item'''
        return self.object_dict.get('UserData', {}).get('IsFavorite', False)

    @async_func
    async def _mark(self, type, value):
        url = '/Users/{{UserId}}/{type}/{id}'.format(type=type, id=self.id)
        if value:
            (await self.connector.post(url)).close()
        else:
            (await self.connector.delete(url)).close()

    @async_func
    async def setFavorite(self, value=True):
        await self._mark('FavoriteItems', value)

    @async_func
    async def setWatched(self, value=True):
        await self._mark('PlayedItems', value)

    @property
    def type(self):
        '''get the object type (general)

        See Also
        --------
          media_type :
        '''
        return self.object_dict.get('Type', 'Object')

    @property
    def media_type(self):
        '''get the object type (specific)

        See Also
        --------
          type :
        '''
        return self.object_dict.get('MediaType', 'Object')

    @property
    def genres(self):
        '''list of genres

        See Also
        --------
          post :
          tags :
        '''
        return self.object_dict.get('Genres', [])

    @genres.setter
    def genres(self, genres: list):
        self.object_dict['Genres'] = genres

    @property
    def tags(self):
        '''list of tags

        See Also
        --------
          post :
          genres :
        '''
        return self.object_dict.get('Tags', [])

    @tags.setter
    def tags(self, tags: list):
        self.object_dict['Tags'] = tags

    @property
    def overview(self):
        '''the description of the item

        See Also
        --------
          post :
        '''
        return self.object_dict.get('Overview', '')

    @overview.setter
    def overview(self, value):
        self.object_dict['Overview'] = value

    @property
    def community_rating(self):
        '''int [0-10] with the rating of the item

        See Also
        --------
          post :
        '''
        return self.object_dict.get('CommunityRating', 0)

    @community_rating.setter
    def community_rating(self, value):
        self.object_dict['CommunityRating'] = value

    @property
    def primary_image_url(self):
        '''url of the main poster image'''
        path = '/Items/{}/Images/Primary'.format(self.id)
        return self.connector.get_url(path, attach_api_key=False)

    @property
    def date(self):
        """alias of premier_date"""
        return self.premier_date

    @date.setter
    def date(self, value):
        self.premier_date = value

    @property
    def premier_date(self):
        """datetime of when the item premiered (aired/released) (or None)"""
        ts = self.object_dict.get('PremiereDate')
        if not ts:
            return None
        return arrow.get(ts).datetime

    @premier_date.setter
    def premier_date(self, value):
        if isinstance(value, datetime.datetime):
            value = value.strftime("%Y-%m-%dT%H:%M:%SZ")
        elif not isinstance(value, str):
            raise ValueError('value must be datetime or str')
        self.object_dict['PremiereDate'] = value

    @property
    def date_created(self):
        """datetime of when the item was added to the server (or None)"""
        ts = self.object_dict.get('DateCreated')
        if not ts:
            return None
        return arrow.get(ts).datetime

    @date_created.setter
    def date_created(self, value):
        if isinstance(value, datetime.datetime):
            value = value.strftime("%Y-%m-%dT%H:%M:%SZ")
        elif not isinstance(value, str):
            raise ValueError('value must be datetime or str')
        self.object_dict['DateCreated'] = value

    @property
    def parent_id(self):
        '''id of the parent object

        See Also
        --------
          parent :
        '''
        return self.object_dict.get('ParentId')

    @property
    @async_func
    async def parent(self):
        '''parent object as a subclass of EmbyObject

        |coro|
        '''
        if self.parent_id:
            return await self.process(self.parent_id)
        else:
            return None

    @property
    def download_url(self):
        return self.connector.get_url('/Items/{}/Download'.format(self.id))

    @property
    @async_func
    async def url(self):
        '''url of the item

        |coro|

        Notes
        -----
          if remote-adderes was given, then that is used as the base
        '''
        if await self.connector.is_jellyfin:
            path = '/web/index.html#!/details?id={}'
        else:
            path = '/web/itemdetails.html?id={}'
        path = path.format(self.id)
        return self.connector.get_url(path, attach_api_key=False)

    @async_func
    async def update(self, fields=''):
        '''reload object info from emby

        |coro|

        Parameters
        ----------
        fields : str
          additional fields to request when updating

        See Also
        --------
          refresh : same thing
          send :
          post :
        '''
        path = 'Users/{{UserId}}/Items/{}'.format(self.id)
        info = await self.connector.getJson(
            path,
            remote=False,
            Fields='Path,Overview,PremiereDate'+(',' if fields else '')+fields
        )
        self.object_dict.update(info)
        self.extras = {}
        return self

    @async_func
    async def refresh(self, fields=''):
        '''Same as update

        |coro|

        See Also
        --------
          update :
        '''
        return await self.update()

    @async_func
    async def send(self):
        '''send data that was changed to emby

        |coro|

        This should be used after using any of the setter.
        Not necessarily immediately, but soon after.

        See Also
        --------
          post: same thing
          update :
          refresh :
        '''
        # Why does the whole dict need to be sent?
        #   because emby is dumb, and will break if I don't
        data = {**_EMPTY_OBJ, **self.object_dict}

        path = 'Items/{}'.format(self.id)
        status, resp = await self.connector.post(
            path,
            data=data,
            remote=False,
            send_raw=True,
            headers={'Content-Type': 'application/json'},
        )
        if status in (400, 415):
            await EmbyObject(self.object_dict, self.connector).update()
            status, resp = await self.connector.post(
                path,
                data=data,
                remote=False,
                send_raw=False,
                headers={'Content-Type': 'application/json'},
            )
        return status, resp

    @async_func
    async def post(self):
        '''Same as send

        |coro|

        See Also
        --------
          send :
        '''
        return await self.send()

    @async_func
    async def process(self, object_dict):
        '''[for internal use] convert json/dict into python object

        |coro|

        Parameters
        ----------
        object_dict : dict
          json representation of object from emby

        Notes
        -----
        if a string is given, it is assumed to be an id, obj is returned.
        if a list is given, this method is called for each item in list.

        Returns
        -------
        EmbyObject
          the object that is represented by the json dict
        list
          if input is a list, list is returned
        '''
        # if ID was given, create dummy object
        # and update it to get full dict
        try:
            if type(object_dict) == str:
                existing = EmbyObject.known_objects.get(object_dict)
                if existing:
                    return existing

                obj = EmbyObject(
                    {"Id": object_dict},
                    self.connector,
                    save=False
                )
                object_dict = (await obj.update()).object_dict
        except:
            return None

        # if nothing was given, return it back
        # if already created object was given, return it back too
        if not object_dict or isinstance(object_dict, EmbyObject):
            return object_dict

        # if a json dict that's really just a list was given,
        #   convert to list
        if type(object_dict) == dict and \
           set(object_dict.keys()).issuperset({'Items', 'TotalRecordCount'}):
            object_dict = object_dict['Items']

        # if a list was given,
        #   process each item in list
        if type(object_dict) == list:
            items = []
            for item in object_dict:
                item = await self.process(item)
                if item:
                    items.append(item)
            return items

        # otherwise we probably have an object dict
        #   so we should process that

        # if dict has no id, it's a fake
        if 'Id' not in object_dict and 'ItemId' not in object_dict:
            return object_dict

        # if object is already stored,
        #   update with existing info and return
        itemId = object_dict.get('Id', object_dict.get('ItemId'))
        existing = EmbyObject.known_objects.get(itemId)
        if existing:
            existing.object_dict.update(object_dict)
            return existing

        import embypy.objects.folders
        import embypy.objects.videos
        import embypy.objects.misc

        # if object is not already stored,
        #   figure out its type (if unknown use this base class)
        #   create an object with subclass of that type
        #   return
        if 'AppName' in object_dict:
            object_dict['Type'] = 'Device'
        elif 'HasPassword' in object_dict:
            object_dict['Type'] = 'User'

        objects = {
            'Audio':		embypy.objects.misc.Audio,
            'Person':		embypy.objects.misc.Person,
            'Video':		embypy.objects.videos.Video,
            'Movie':		embypy.objects.videos.Movie,
            'Trailer':		embypy.objects.videos.Trailer,
            'AdultVideo':	embypy.objects.videos.AdultVideo,
            'MusicVideo':	embypy.objects.videos.MusicVideo,
            'Episode':		embypy.objects.videos.Episode,
            'Folder':		embypy.objects.folders.Folder,
            'Playlist':		embypy.objects.folders.Playlist,
            'BoxSet':		embypy.objects.folders.BoxSet,
            'MusicAlbum':	embypy.objects.folders.MusicAlbum,
            'MusicArtist':	embypy.objects.folders.MusicArtist,
            'Season':		embypy.objects.folders.Season,
            'Series':		embypy.objects.folders.Series,
            'Game':		embypy.objects.misc.Game,
            'GameSystem':	embypy.objects.folders.GameSystem,
            'Photo':		embypy.objects.misc.Photo,
            'Book':		embypy.objects.misc.Book,
            'Image':		embypy.objects.misc.Image,
            'Device':		embypy.objects.misc.Device,
            'User':		embypy.objects.misc.User,
            'Default':		EmbyObject,
        }
        return objects.get(
            object_dict.get('Type', 'Default'),
            EmbyObject
        )(object_dict, self.connector)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<{} {}>'.format(self.type, self.id)

    @property
    def provider_ids(self):
        res = self.object_dict.get("ProviderIds", {})
        return res

    @property
    def tmdbid(self):
        return self.provider_ids.get("Tmdb")

    @property
    def imdbid(self):
        return self.provider_ids.get("Imdb")
