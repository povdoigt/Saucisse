import urllib.request
import re
from pytubefix import YouTube
import os
code_path =  'C:/Users/Malo/Documents/bot_Saucisse/ '

def get_url(search_query):
    url = "https://www.youtube.com/results?search_query=" + search_query

    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')

    video_ids = re.findall(r'watch\?v=(\S{11})', html)

    video_urls = ["https://www.youtube.com/watch?v=" + video_id for video_id in video_ids]

    return video_urls[0]


def download_video(url):
    # url input from user
    yt = YouTube(str(url))

    # extract only audio
    video = yt.streams.filter(only_audio=True).first()

    # check for destination to save file

    # download the file
    out_file = video.download(output_path='C:/Users/Malo/Documents/bot_Saucisse/')

    # save the file

    print(out_file)
    # result of success
    print(yt.title + " has been successfully downloaded.")
    return out_file 


def get_video(search):
    title = download_video(get_url(search))
    return title 

def get_video_with_link(link):
    print(link)
    title = download_video(link)
    return title

