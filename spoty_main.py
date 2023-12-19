#from dotenv import load_dotenv, find_dotenv
from requests import get
import random
from os import path
from pygame import mixer
import time
from spoty_functions import compute_energy, get_token, get_auth_header, get_features, search_for_song, send_OSCmessage
import webbrowser
import json
import numpy as np
import os


'''path='C:/Users/lelio/OneDrive/Desktop/CPAC project/.env'

load_dotenv(dotenv_path=path,verbose=True)'''


def spotify_search (song_name, client_id, client_secret, query_limit, path):
    
    token = get_token(client_id, client_secret)
    song_ids, song_urls = search_for_song(token, song_name, query_limit)
    random_num = random.randint(0, len(song_ids)-1)
    chosen_id = song_ids[random_num]
    get_features(token, chosen_id)

    
    download_url = song_urls[random_num]
    response = get(download_url)

    # Save as wav file
    with open('song.mp3', 'wb') as s:
        s.write(response.content)

    energy_data = compute_energy('song.mp3')
    print(energy_data)
    if not isinstance(energy_data, np.ndarray):
        energy = np.array(energy_data)

    energy_data = {
        'values': energy.tolist()
    }

    with open('data.js', 'w') as f:
        f.write('const data = '+json.dumps(energy_data))
   
    webbrowser.open('file://' + os.path.realpath('index_graph.html'))
  


    """
    open(path, "wb").write(response.content)
    
    get_energy_data(path)
    mixer.init()
    mixer.music.load(path)
    #return render_template('index_graph.html', download_url=download_url)
    
    mixer.music.play()
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(1)
    #mixer.quit()
    """
