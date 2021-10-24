from __future__ import unicode_literals
from omxplayer.player import OMXPlayer

import youtube_dl

def extract_info_from_url(url, ovverride_args = {}):
    """
        Returns selected info as a dictionary from a given youtube url

        Arguments:
        url - a youtube-dl compatible url as a string
        override_args - overrides youtube-dl args such as {'format':'bestvideo[ext=mp4]+bestvideo[height<=480]+bestaudio/best[height<=480]'}

        Returns:
        info_dict - a dictionary of return values with attributes best
        accessible via info_dict.get("attr", None). Attributes:
            url - the direct url of the video
            title - the string title of the video
            id - the unique id of the video
            
    """
    ydl_opts = {'simulate':True, 'forceurl':True, 'forcetitle':True, 'format':'mp4'}
    ydl_opts.update(ovverride_args)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download = False)
    return info

def extract_info_from_search(search, ovverride_args = {}):
    """
        See @extract_info_from_url

        Argument change:
        search <- url - a search string used to query youtube
    """

    url = "ytsearch:" + search
    return extract_info_from_url(url, ovverride_args)

def play_video_url(url, callback):
    """
        Displays the video from a direct url.

        Arguments:
        url - a direct video url that points to a filename (preferably mp4 for rpi)
        callback - a function that will be called upon video termination

        Returns:
        player - an omxplayer object that can be terminated early using player.quit()
    """

    player = OMXPlayer(url)
    player.exitEvent += callback
    return player