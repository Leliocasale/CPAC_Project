#from dotenv import load_dotenv, find_dotenv
from requests import get
import random
from os import path
from pygame import mixer
import time
from spoty_functions import gesture, compute_energy, get_token, get_auth_header, get_features, search_for_song, send_OSCmessage


'''path='C:/Users/lelio/OneDrive/Desktop/CPAC project/.env'

load_dotenv(dotenv_path=path,verbose=True)'''


client_id = "b3a47786876e4b3caf05c32b0bf2feea"
client_secret = "f7021e75f1144c0fa6ccade8bfbf8ce8"
query_limit = 10
song_name = "Born Yesterday"
path = "selectedSong"

def spotify_search (song_name, client_id, client_secret, query_limit, path):
    token = get_token(client_id, client_secret)
    song_ids, song_urls = search_for_song(token, song_name, query_limit)
    random_num = random.randint(0, len(song_ids)-1)
    chosen_id = song_ids[random_num]
    get_features(token, chosen_id)
    download_url = song_urls[random_num]
    response = get(download_url)
    open(path, "wb").write(response.content)
    compute_energy(path)
    mixer.init()
    mixer.music.load(path)
    mixer.music.play()
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(1)

spotify_search(song_name, client_id, client_secret, query_limit, path)
