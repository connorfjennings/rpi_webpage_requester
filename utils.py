from __future__ import unicode_literals
import subprocess

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
    ydl_opts = {'simulate':True, 'forceurl':True, 'forcetitle':True, 'format':'[ext=mp4][height<=480]'}
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
    all_vids = extract_info_from_url(url, ovverride_args)
    return all_vids.get('entries')[0]

def play_video_url(url):
    """
        Displays the video from a direct url.

        Arguments:
        url - a direct video url that points to a filename (preferably mp4 for rpi)

        Returns:
        process - a subprocess that must be terminated before calling this function again.
    """
    
    process = subprocess.Popen(["vlc", "-f", url])
    return process
