from musicsync import MusicSync
import glob
import os

ms = MusicSync("bmjsmith@gmail.com")

os.chdir("g:/public/music")
for m3ufile in glob.glob("*.m3u"):
    print "Found: " + m3ufile
    ms.sync_playlist("g:/public/music/" + m3ufile)
