import urllib.request
import json
import os
import numpy as np

working_directory = ''
channel_file = ''
key = '' #api key


def search_videos(Channle_id): # gets the channel data
    r = urllib.request.urlopen('https://www.googleapis.com/youtube/v3/search?key=' + key + '&channelId=' + Channle_id + '&part=snippet,id&order=date&maxResults=30')
    return r

def search_live_videos(Channle_id): # gets the channel data
    r = urllib.request.urlopen('https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=' + Channle_id + '&eventType=live&type=video&key=' + key)
    return r

def search_channel(Channle_name): #looks up the chaanle Id from username
    try:
        r = urllib.request.urlopen('https://www.googleapis.com/youtube/v3/channels?part=id&forUsername=' + Channle_name + '&key=' + key)
        data_string = json.loads(r.read().decode())
        items = data_string['items']
        dict = items[0]
        Id = dict['id']
        print("the channle ID is " + Id)
        return str(Id) #conv to string
    except:
        print('error to search channel name ' + Channle_name)
        return(0)

def filter_video_ids(json_file): #extracts video Ids
    Ids = []
    data_string = json.loads(json_file.read().decode())
    items = data_string['items'] #gets the videos
    for x in range(len(items)): #runs through the array
        video = items[x]
        Ids.append(video['id']['videoId'])
    return (Ids) #returns a list of ids

def load_channels():
    channels = open("channels.txt","r")
    lines = channels.read().split(',')
    channels.close()
    return(lines)
    print('placeholder')

def create_new_directory(current_channel): # chreats a new video direcotry for a channle and creates an "ids" file
    os.mkdir(working_directory + current_channel)
    os.chdir(working_directory + current_channel)
    new_channel = open("downloaded_ids.txt","w+")
    new_channel.close()
    print('sucsessfully created directory for ' + current_channel)

def create_new_live_directory(current_channel):
    os.mkdir(working_directory + current_channel)
    print('sucsessfully created directory for ' + current_channel)

def check_directory(current_channel): #checks if the channel directory esists
    directroy_exists = os.path.isdir(working_directory + current_channel)
    return(directroy)

def change_directory(current_channel): #changes  the current directory to the specified chanlles or live
    try:
        os.chdir(working_directory + current_channel)
    except:
        return('error')

def compare_ids(Video_ids):
    print('placeholder')

def add_id(Video_id):
    print('placeholder')

def download_video(video_id):
    print('placeholder')

def download_live(video_id):
    print('placeholder')



id = search_channel('disneyjunretior')
if id == 0:
    print('skipping')
else:
    Videos = search_live_videos(id)
    Videos_id = filter_video_ids(Videos)
    print(Videos_id)

