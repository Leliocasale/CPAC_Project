from dotenv import load_dotenv, find_dotenv
import base64
from requests import post, get
import json
import random
from os import path
from pygame import mixer
import time
import librosa
from pythonosc import udp_client
import numpy as np
from pythonosc.udp_client import SimpleUDPClient
#from parse_gesture import gesture, compute_energy

'''path='C:/Users/lelio/OneDrive/Desktop/CPAC project/.env'

load_dotenv(dotenv_path=path,verbose=True)'''


client_id = "b3a47786876e4b3caf05c32b0bf2feea"
client_secret = "f7021e75f1144c0fa6ccade8bfbf8ce8"
query_limit = 10
song_name = "Born Yesterday"
path = "selectedSong"

def gesture(code):
    if code == 0:
        song_name = "I love you"
    if code == 1:
        song_name = "I remember"

def compute_energy(songPath):
    song_signal, sampleRate = librosa.load(songPath) #load song
    #print(sampleRate)
    #song_dur = librosa.get_duration(y = song_signal, sr = sampleRate) #compute duration
    #print(song_dur)
    hop_length = 256
    frame_length = 512
    numberOfHops = len(song_signal)//hop_length 
    print(numberOfHops)
    inst_energy = [] #create empty list
    padded_signal = np.pad(song_signal, (0, ((numberOfHops+1)*hop_length)-len(song_signal)), 'constant') #zero padding
    print(len(song_signal))
    print(len(padded_signal))
    #print(padded_signal[0])
    for i in range(numberOfHops-1):
        computed_energy = sum(abs((padded_signal[(i*hop_length):(i*hop_length+frame_length-1)])**2))
        inst_energy.append(computed_energy)
    print(len(inst_energy))


#create valid token for a spotify request
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"

    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

#create correct header for a specific token
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search_for_song(token, song_name):
    #formulate request
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={song_name}&type=track&limit=" + str(query_limit)
    query_url = url + "?" + query
    #send request to spotify and store response
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)

    ids = []
    song_urls = []
    #take ids and urls of the found songs
    for i in range(query_limit):
        if json_result["tracks"]["items"][i]["preview_url"] != None: #some songs have as preview url 'None' -> in this case the song cannot be played 
            ids.append(json_result["tracks"]["items"][i]["id"])
            song_urls.append(json_result["tracks"]["items"][i]["preview_url"])
    #print(json_result)
    print(len(ids))
    return ids, song_urls

def get_features(token, id):
    url="https://api.spotify.com/v1/audio-features/" + id
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_features = json.loads(result.content)
    print(json_features)



def send_OSCmessage(message, hopNum, frameSize, sampleRate):
    ip = "127.0.0.1"
    port = 1337
    client = udp_client.SimpleUDPClient(ip, port)  # Create client
    client.send_message("/energyAtTime/" + hopNum*(frameSize/sampleRate), message)


token = get_token()
song_ids, song_urls = search_for_song(token, song_name)
random_num = random.randint(0, len(song_ids)-1)
chosen_id = song_ids[random_num]
get_features(token, chosen_id)
download_url = song_urls[random_num]
response = get(download_url)
open(path, "wb").write(response.content)
mixer.init()
mixer.music.load(path)
mixer.music.play()
while mixer.music.get_busy():  # wait for music to finish playing
    time.sleep(1)
compute_energy(path)
#gesture(0)