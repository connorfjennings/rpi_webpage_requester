from __future__ import unicode_literals
import youtube_dl

ydl_opts = {'simulate':True, 'forceurl':True, 'forcetitle':True, 'format':'mp4'}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.extract_info(['https://www.youtube.com/watch?v=BaW_jenozKc'])

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

