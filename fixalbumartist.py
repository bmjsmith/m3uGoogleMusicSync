"""
    fixalbumartist.py

    Provides a simple class which will go through your google music library
    and copy the artist to albumartist where albumartist is empty

    API used: https://github.com/simon-weber/Unofficial-Google-Music-API
    Thanks to: Kevion Kwok and Simon Weber

    Usage:
     aa = AlbumArtist()
     # Will prompt for Email and Password - if 2-factor auth is on you'll need to generate a one-
       time password

     aa.fix_album_artist()

"""

from gmusicapi.api import Api
from getpass import getpass

MAX_UPLOAD_ATTEMPTS_PER_FILE = 3
MAX_CONNECTION_ERRORS_BEFORE_QUIT = 5
STANDARD_SLEEP = 5

class AlbumArtist(object):
    def __init__(self, email=None, password=None):
        self.api = Api()
        if not email:
            email = raw_input("Email: ")
        if not password:
            password = getpass()

        self.email = email
        self.password = password

        self.logged_in = self.auth()


    def auth(self):
        self.logged_in = self.api.login(self.email, self.password)
        if not self.logged_in:
            print "Login failed..."
            exit()

        print ""
        print "Logged in as %s" % self.email
        print ""


    def fix_album_artist(self):

        def noAlbumArtist(x): return len(x['albumArtist']) == 0

        def fixSong(song):
            song['albumArtist'] = song['artist']
            return song

        def chunks(l, n):
            """ Yield successive n-sized chunks from l.
            """
            for i in xrange(0, len(l), n):
                yield l[i:i+n]

        songs = filter(noAlbumArtist, self.api.get_all_songs())

        print "Found %d songs that have no albumArtist" % len(songs)

        fixedSongs = map(fixSong, songs)

        fixedSongChunks = chunks(fixedSongs, 100)

        map(self.api.change_song_metadata, fixedSongChunks)

        print "Fixed %d songs" % len(fixedSongs)

