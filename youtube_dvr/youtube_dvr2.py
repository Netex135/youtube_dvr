from __future__ import unicode_literals #imports youtube_dl
import json
import os
import numpy as np
import sys
import subprocess
import time
from multiprocessing import Pool
from multiprocessing import Process
import requests


import youtube_dl

download_directory = '/share/' #directroy of where to download Videos
working_directory = os.getcwd()
seconds_for_download = 80000


def search_videos(Channle_id): # gets the channel data
        r = requests.get('https://www.googleapis.com/youtube/v3/search?key=' + key + '&channelId=' + Channle_id + '&part=snippet,id&order=date&maxResults=30')
    #    print(r.json())
        print(type(r.json()))
        return r.json()

def search_live_videos(Channle_id): # gets the channel data
    r = requests.get('https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=' + Channle_id + '&eventType=live&type=video&key=' + key)
    print(r.json())
    return r.json()

def search_channel(Channle_name): #looks up the chaanle Id from username
    try:
        print('http://www.googleapis.com/youtube/v3/channels?part=id&forUsername=' + Channle_name + '&key=' + key)
        r = http.request('GET', 'https://www.googleapis.com/youtube/v3/channels?part=id&forUsername=' + Channle_name + '&key=' + key)

        data_string = json.loads(r.read().decode('utf-8'))
        items = data_string['items']
        dict = items[0]
        Id = dict['id']
        print("the channle ID is " + Id)
        return str(Id) #conv to string
    except:
        print('error to search channel name ' + Channle_name)
        return(0)

def filter_video_ids(json_file): #extracts video Ids from Json files
    Ids = []                     #video Ids
#    data_string = json.loads(json_file.read().decode('utf-8'))

    #data_string = json.loads(json_file.read().decode())
    items = json_file['items'] #gets the videos
    for x in range(len(items)): #runs through the array
        video = items[x]
        try:
            Ids.append(video['id']['videoId'])
        except:
            print("no video id")
    return(Ids) #returns a list of ids

def load_file(filename):        # gets the contents a file and returns it as a list
    file = open(filename + ".txt","r")
    data = file.read().split(',') #sperates the file into a list by ,
    file.close()
    return(data)

def create_new_directory(current_channel): # creates a new video direcotry for a channle and creates an "ids" file
    os.mkdir(download_directory + current_channel)
    os.chdir(download_directory + current_channel)
    new_channel = open("downloaded_ids.txt","w+")
    new_channel.close()
    print('sucsesfully created directory for ' + current_channel)

def create_new_live_directory(current_channel): # creates a new dictionary for a channel that is being tracked for livestreams
    os.mkdir(dowload_directory + current_channel + '_live')
    print('sucsessfully created directory for ' + current_channel)

def check_video_directory(current_channel): #checks if the channel directory esists
    directroy_exists = os.path.isdir(download_directory + current_channel)
    return(directroy_exists)

def change_channel_directory(current_channel): #changes  the current directory to the specified chanlles or live
    os.chdir(download_directory + current_channel)


def compare_ids(downloaded_ids, current_ids):   #compares two arrays and return objects that aren't present in the second
    difference = np.setdiff1d(current_ids,downloaded_ids)
    return(difference)

def add_id(video_id):   #adds the downloaded id to the channle's file
    with open("downloaded_ids.txt", "a") as myfile:
        myfile.write(video_id + ",")

def download_video(video_id): #downloads video
    try:
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://www.youtube.com/watch?v='+video_id])
        #subprocess.run(["youtube-dl","-f best", "https://www.youtube.com/watch?v=" + video_id])
        add_id(video_id)
        #subprocess.run(["youtube-dl","-f best", "https://www.youtube.com/watch?v=" + video_id])
    except:
        try:
            subprocess.run(["youtube-dl","-f best", "https://www.youtube.com/watch?v=" + video_id])
        except:
            print("could not download video")

def download_live(video_id): #downloads live stream
    subprocess.run(["youtube-dl","-o '%(view_count)s.%(title)s.%(ext)s'", "-v -f 96/95/301/300 https://www.youtube.com/watch?v=" + video_id])
    print('placeholder')

def load_key():     #loads the api key
    key = str(load_file('key')[0])
    key = key[1:-1] # remove the ('')
    return(key)

def load_channels(): # reads the current channels downloaded videos
    data = {} # dictrionarry with channels and ids
    with open('channels.txt','r') as inf:   #loads file as dictionarry
        data = eval(inf.read()) # reads the channel dictionarry and stores them in data
    return data

def load_live_channels():
    data = {} # dictrionarry with channels and ids
    with open('live_channels.txt','r') as inf:   #loads file as dictionarry
        data = eval(inf.read())
    return data

def initailize():   #creates video files which don't exist
    if (check_video_directory('')):
        channel_data = load_channels() # loads raw channels
        channels = list(channel_data.keys()) # gets the names of channels from the key in a list
        print(channels) # testing
        print('loaded channels ' + str(channels))
        for channel in range(len(channels)): #checks every channel that was loaded
            directory_exists = check_video_directory(channels[channel])
            if (directory_exists == False): #checks directory and if it doesnt exist creats a new one
                print('creating directory for' + channels[channel])
                create_new_directory(channels[channel])
    else:
        print('warning! download directory path does not exist: exiting')
        sys.exit(1)

def download_sort_videos(): # get download and short videos from youtube channels defined in channels.txt
    global key
    global ydl_opts
    ydl_opts = {
    'format': 'best',
    }
    key = load_key()
    channel_data = load_channels()
    channel_names = list(channel_data.keys())
    print(channel_names)
    while (True):
        for name in range(len(channel_names)):
            print(channel_data[channel_names[name]])
            try:
                videos = search_videos(channel_data[channel_names[name]])
                new_ids = filter_video_ids(videos)
                print(new_ids)
                try:
                    change_channel_directory(channel_names[name])
                    downloaded_ids = load_file('downloaded_ids')
                    needed_ids = compare_ids(downloaded_ids, new_ids)
                    print('need to download ' + str(needed_ids))
                    for id in range(len(needed_ids)):
                        download_video(needed_ids[id])
                except:
                    print("can't change directory skipping " + channel_names[name])
            except:
                print("couldn't search video")
        time.sleep(seconds_for_download)

def initailize_live():   #creates video files which don't exist
    if (check_video_directory('')): #checks if the dictionarry set exists before writing
        channel_data = load_live_channels()
        channels = list(channel_data.keys())
        print(channels)
        print('loaded channels ' + str(channels))
        for channel in range(len(channels)):
            directory_exists = check_video_directory(channels[channel] + "_live")
            if (directory_exists == False):
                print('creating directory for' + channels[channel])
                create_new_live_directory(channels[channel])
            #    create_new_directory(channels[channel] + "_live")
    else:
        print('warning! download directory path does not exist: exiting')
        sys.exit(1) #exits


#def download__remove_live_videos(name,live_stream_id):
#    try:
#        change_channel_directory(channel_names[name] + "_live")
#        print('need to download ' + str(live_stream_id))
#        del channel_data[name]
#        for id in range(len(live_stream_id)):
#            download_video(live_stream_id[id])
#        channel_data[name] =
#    except:
#        print("can't change directory skipping " + channel_names[name])

def download_sort_live_videos(): # get download and short videos from youtube channels defined in channels.txt
    global key                     #gets the api key
    global channel_data
    global channel_names
    key = load_key()
    channel_data = load_live_channels()
    channel_names = list(channel_data.keys())
    while True:
        for name in range(len(channel_names)):
            # print(channel_data[channel_names[name]])
            time.sleep((10))
            try:
                print("searching " + channel_names[name]) #pritns the channel that is being searched
                live_stream = search_live_videos(channel_data[channel_names[name]])
                live_stream_id = filter_video_ids(live_stream)
                if live_stream_id != []:
                    try:
                        change_channel_directory(channel_names[name] + "_live")
                        print('need to download ' + str(live_stream_id))
                        for id in range(len(live_stream_id)):
                            download_live(live_stream_id[id])
                    except:
                        print("can't change directory skipping " + channel_names[name])
            except:
                print("couldn't search video")


if __name__ == '__main__':
        key = load_key() #loads the api key
        initailize() #creats the iles for new channels
        initailize_live() #creates files for new live channels
        channel_data = load_channels()
        channel_names = list(channel_data.keys())
        d_s_v = Process(target=download_sort_videos, args=())
        d_s_v.start()
        download_sort_live_videos()
