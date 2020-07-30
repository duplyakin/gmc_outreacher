import cloudinary
import cloudinary.uploader
import cloudinary.api
from pytube import YouTube
import os
import shutil
import math
import datetime
import urllib

#Barry
#DOWNLOAD_VIDEO = 'https://youtu.be/L9gVrDsQ2BQ'
#PUBLIC_ID = 'barry_video_for_test'
#UPLOAD_FILENAME = 'barry_video.mp4'

#random guy
#gif url: https://res.cloudinary.com/dfhw5en5v/video/upload/c_scale,e_boomerang,eo_5,h_281,so_0,w_500/e_loop/random_guy_test.gif
# video url: http://res.cloudinary.com/dfhw5en5v/video/upload/v1595329379/random_guy_test.mp4
# with subtitles: http://res.cloudinary.com/dfhw5en5v/video/upload/l_subtitles:random_guy_test.transcript/random_guy_test.mp4
# uploaded mp3 url: http://res.cloudinary.com/dfhw5en5v/video/upload/v1595345079/random_guy_test_audio.mp3

DOWNLOAD_VIDEO = 'https://www.youtube.com/watch?v=bbyhj8rkzJc'
PUBLIC_ID = 'random_guy_test'
GIF_PUBLIC_ID = 'random_guy_test_gif'
AUDIO_PUBLIC_ID = 'random_guy_test_audio'

SUBTITLES_PUBLIC_ID = PUBLIC_ID + '.transcript'
UPLOAD_FILENAME = 'random_video.mp4'
GIF_FILE_PATH = './random_guy_test.gif'
MP3_FILE_PATH = './random_guy_test.mp3'

GIT_URL = 'https://res.cloudinary.com/dfhw5en5v/video/upload/c_scale,e_boomerang,eo_5,h_281,so_0,w_500/e_loop/random_guy_test.gif'
MP3_URL = 'https://d1490khl9dq1ow.cloudfront.net/audio/music/mp3preview/BsTwCwBHBjzwub4i4/bnm-0715-after-all-stinger_NWM.mp3'

cloudinary.config( 
  cloud_name = "dfhw5en5v", 
  api_key = "739984578374586", 
  api_secret = "W40nleOKaNVAtyXRtYffaHa72EA" 
)

def info_youtube_video(url):
    video = YouTube(url)
    streams = video.streams.all()
    print(streams)

def download_youtube_video(url):
    video = YouTube(url)
    downloaded = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').asc().first().download()

def upload_video_subtitles(file_name):
    res = cloudinary.uploader.upload(file_name,
                                    resource_type = "video",
                                    public_id = PUBLIC_ID,
                                    raw_convert = "google_speech")
    print(res)

def upload_video(file_name):
    res = cloudinary.uploader.upload(file_name,
                                    resource_type = "video",
                                    public_id = PUBLIC_ID)
    print(res)


def video_subtitles_url(public_id):
    res = cloudinary.CloudinaryVideo(PUBLIC_ID).video(overlay={'resource_type': "subtitles", 'public_id': SUBTITLES_PUBLIC_ID})
    print(res)


def generate_gif_with_subtitles(width=500, height=281):
    GIF_FILENAME = PUBLIC_ID + ".gif"
    res = cloudinary.CloudinaryVideo(GIF_FILENAME).image(transformation=[
        {'width': width, 'height' : height, 'start_offset': "0", 'end_offset': "5", 'effect': "boomerang", 'crop': "scale"},
        {'effect': "loop"}
    ])
    print(res)

def download_gif_file(url, file_path=GIF_FILE_PATH):
    urllib.request.urlretrieve(url, file_path)

def download_mp3_file(url, file_path=MP3_FILE_PATH):
    urllib.request.urlretrieve(url, file_path)

def upload_gif_file(url):
    res = cloudinary.uploader.upload(url,
                                    resource_type = "image",
                                    public_id = GIF_PUBLIC_ID,
                                    flags="lossy",
                                    quality=50)
    print(res)

def gif_add_subtitles(public_id, text):
    GIF_FILE = public_id + '.gif'
    res = cloudinary.CloudinaryImage(GIF_FILE).image(transformation=[
            {'width' : 440,  'overlay': {'font_family': "Times", 'font_size': 10, 'text_align' : 'center', 'text': text, 'crop': 'fit'}, 'gravity': "south", 'y': 20, 'color': "#FFFFFF"}
        ])

    print(res)


def upload_audio_file(file_name):
    res = cloudinary.uploader.upload(file_name,
                                    resource_type = "video",
                                    public_id = AUDIO_PUBLIC_ID)
    print(res)

def change_audio(audio_public_id, video_public_id):
    overlay_audio = 'video:' + audio_public_id
    res = cloudinary.CloudinaryVideo(video_public_id).video(transformation=[
        {'overlay' : overlay_audio, 'start_offset' : '0', 'end_offset' : '5'}
    ])
    print(res)

#download_youtube_video(url=DOWNLOAD_VIDEO)
#info_youtube_video(url=DOWNLOAD_VIDEO)
#upload_video(file_name=UPLOAD_FILENAME)
#video_subtitles_url(public_id=PUBLIC_ID)
#generate_gif_with_subtitles()
#download_gif_file(GIT_URL)
#upload_gif_file(GIT_URL)
#gif_add_subtitles(public_id=GIF_PUBLIC_ID, text="Hi Barry! I like the outreacher24. Would you like to talk on sunday?")
#download_mp3_file(url=MP3_URL)
#upload_audio_file(file_name=MP3_FILE_PATH)
change_audio(audio_public_id=AUDIO_PUBLIC_ID, video_public_id=PUBLIC_ID)