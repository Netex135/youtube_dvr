import urllib.request
import json
import os
import numpy as np
import sys
import subprocess
import time
from multiprocessing import Pool
from multiprocessing import Process

dowload_directory = 'C:\\Users\\orcmi\\OneDrive\\Documents\\test\\' #directroy of where to download Videos
working_directory = os.getcwd()
seconds_for_download = 8000


def search_videos(Channle_id): # gets the channel data
    r = urllib.request.urlopen('https://www.googleapis.com/youtube/v3/search?key=' + key + '&channelId=' + Channle_id + '&part=snippet,id&order=date&maxResults=30')
    return r

def search_live_videos(Channle_id): # gets the channel data
    r = urllib.request.urlopen('https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=' + Channle_id + '&eventType=live&type=video&key=' + key)
    return r

def search_channel(Channle_name): #looks up the chaanle Id from username
    try:
        print('https://www.googleapis.com/youtube/v3/channels?part=id&forUsername=' + Channle_name + '&key=' + key)
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
    Ids = []                     #video Ids
    data_string = json.loads(json_file.read().decode())
    items = data_string['items'] #gets the videos
    for x in range(len(items)): #runs through the array
        video = items[x]
        Ids.append(video['id']['videoId'])
    return (Ids) #returns a list of ids

def load_file(filename):        # gets the contents a file
    file = open(filename + ".txt","r")
    data = file.read().split(',')
    file.close()
    return(data)

def create_new_directory(current_channel): # chreats a new video direcotry for a channle and creates an "ids" file
    os.mkdir(dowload_directory + current_channel)
    os.chdir(dowload_directory + current_channel)
    new_channel = open("downloaded_ids.txt","w+")
    new_channel.close()
    print('sucsessfully created directory for ' + current_channel)

def create_new_live_directory(current_channel):
    os.mkdir(dowload_directory + current_channel + '.live')
    print('sucsessfully created directory for ' + current_channel)

def check_video_directory(current_channel): #checks if the channel directory esists
    directroy_exists = os.path.isdir(dowload_directory + current_channel)
    return(directroy_exists)

def change_channel_directory(current_channel): #changes  the current directory to the specified chanlles or live
        os.chdir(dowload_directory + current_channel)


def compare_ids(downloaded_ids, current_ids):   #compares two arrays and return objects that aren't present in the second
    difference = np.setdiff1d(current_ids,downloaded_ids)
    return(difference)

def add_id(video_id):   #adds the downloaded id to the channle's filek
    with open("downloaded_ids.txt", "a") as myfile:
        myfile.write(video_id + ",")

def download_video(video_id):
    subprocess.run(["youtube-dl", "https://www.youtube.com/watch?v=" + video_id])
    add_id(video_id)

def download_live(video_id):
    print('placeholder')

def load_key():     #loads the api key
    key = str(load_file('key')[0])
    key = key[1:-1]
    return(key)

def load_channels():
    data = {} # dictrionarry with channels and ids
    with open('channels.txt','r') as inf:   #loads file as dictionarry
        data = eval(inf.read())
    return data

def load_live_channels():
    data = {} # dictrionarry with channels and ids
    with open('live_channels.txt','r') as inf:   #loads file as dictionarry
        data = eval(inf.read())
    return data

def initailize():   #creates video files which don't exist
    if (check_video_directory('')):
        channel_data = load_channels()
        channels = list(channel_data.keys())
        print(channels)
        print('loaded channels ' + str(channels))
        for channel in range(len(channels)):
            directory_exists = check_video_directory(channels[channel])
            if (directory_exists == False):
                print('creating directory for' + channels[channel])
                create_new_directory(channels[channel])
    else:
        print('warning! download directory path does not exist: exiting')
        sys.exit(1)

def download_sort_videos(): # get download and short videos from youtube channels defined in channels.txt
    global key
    key = load_key()
    while True:
        channel_data = load_channels()
        channel_names = list(channel_data.keys())
        for name in range(len(channel_names)):
            # print(channel_data[channel_names[name]])
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
        time.sleep(seconds_for_download)

#id = search_channel('disneyjunior')
#if id == 0:
#    print('skipping')
#else:
#    Videos = search_live_videos(id)
#    Videos_id = filter_video_ids(Videos)
#    print(Videos_id)
#print(Videos.read())

if __name__ == '__main__':

        key = load_key()
        initailize()
        channel_data = load_channels()
        channel_names = list(channel_data.keys())
        d_s_v = Process(target=download_sort_videos, args=())
        d_s_v.start()
        d_s_v.join()

#id = 'UCLThzQLfSpLuHimpT1MlcQQ'
#if id == 0:
#    print('skipping')
#else:
#    Videos = search_live_videos(id)
#    Videos_id = filter_video_ids(Videos)
#    print(Videos_id)
#print(Videos.read())
