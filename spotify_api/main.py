import requests
from collections import Counter

from auth import Auth

base_url = 'https://api.spotify.com/v1/'

auth = Auth()
token = auth.get_token()

headers = {
    'Authorization': f'Bearer {token}',
    "Accept": "application/json"
}

search = requests.utils.quote("album:Blackstar")

params = {
    'type' : "album",
    'q' : search
}

response = requests.get(base_url+"search", headers=headers, params=params)

if response:
    pass
    #print(response.json())
else:
    print(f"Error {response.status_code}")
    print(response.content)

albums = response.json()["albums"]["items"]
first_album = albums[0]
artist = first_album["artists"][0]
artist_id = artist['id']

#############
# Mi codigo

### URLS
artistas_mas_escuchados = 'me/top/artists'
canciones_mas_escuchados = 'me/top/tracks'
playlist_legendary = 'playlists/37i9dQZF1DWWGFQLoP9qlv/tracks'
audio_features_url = 'audio-features'

params = {
    'time_range' : "long_term",
    'limit' : 10
}

#response = requests.get(base_url+"artists/"+artist_id, headers=headers, params=params)
response = requests.get(base_url+artistas_mas_escuchados, headers=headers, params=params)

if response:    
    pass
    #print(response.text)
else:
    print(f"Error {response.status_code}")
    print(response.content)

#print(response.json()["items"][9]['name'])

def top_10():

        response = requests.get(base_url+artistas_mas_escuchados, headers=headers, params=params)
        '''
        Los 10 artistas más escuchados por el usuario
        - A través de esos 10 artistas, obtener una lista de los 5 géneros musicales favoritos de dicho usuario
        '''
        counter = 0
        list_genres = []
        print('Los 10 artistas más escuchados por el usuario')
        for i in response.json()["items"]:
            for clave , valor in i.items():
                if clave == 'name':
                    print(counter, ':', valor)
                if clave == 'genres':
                    for i in valor:
                        list_genres.append(i)
                    counter_list_genres = Counter(list_genres).most_common(5)
                    counter +=1
        
        print('-------------------------------------')
        print('Los 5 géneros musicales favoritos')                              
        for index, value in enumerate(counter_list_genres):
             print(index + 1, value[0])
        print('-------------------------------------')
        '''
        Las 10 canciones más escuchadas por el usuario y sus respectivos artistas
        '''
        response = requests.get(base_url+canciones_mas_escuchados, headers=headers, params=params)
        top_listen = {}
        for i in range(params['limit']):
            track_name_dict = response.json()["items"][i]["name"]
            top_listen[track_name_dict] = []
            artist_names = response.json()["items"][i]["album"]["artists"]
            for i in artist_names:
                for track_name, artist_name in i.items():
                    if track_name == 'name':
                        top_listen[track_name_dict].append(artist_name)
        print('Las 10 canciones más escuchadas por el usuario y sus respectivos artistas')
        for clave, valor in top_listen.items():
            print(clave, ':', str(valor)[1:-1].replace("'", ""))            
                    
def play_list_audio_features():
    print('-------------------------------------')
    print('Valor medio de los siguientes parámetros de todas sus canciones')   
    list_tracks_id = []
    response = requests.get(base_url+playlist_legendary, headers=headers)
    playlist_length =  len(response.json()["items"]) 
    for i in range(playlist_length):
        tracks_id = response.json()["items"][i]["track"]["id"]
        list_tracks_id.append(tracks_id)
        ## unpacking the list in the variable
    playlist_params = "ids="+",".join(list_tracks_id) 
    list_tracks_id = ",".join(list_tracks_id) 
    playlist_reponse = requests.get(base_url+audio_features_url, headers=headers, params=playlist_params)
    audio_features = ['tempo','acousticness','danceability','energy','instrumentalness','liveness','loudness','valence']
    result = 0
    count = 0
    for feature in audio_features:
        for i in range(playlist_length):
            count += 1
            result += playlist_reponse.json()["audio_features"][i][feature]
        result = result / playlist_length
        print(feature,':', result )
        result = 0
    print('-------------------------------------')
    count           =0
    tempo           =0
    acousticness    =0 
    danceability    =0
    energy          =0
    instrumentalness=0
    liveness        =0
    loudness        =0
    valence         =0
    for i in range(playlist_length):
        tempo += playlist_reponse.json()["audio_features"][i]['tempo']
        count += 1
        acousticness += playlist_reponse.json()["audio_features"][i]['acousticness']
        danceability += playlist_reponse.json()["audio_features"][i]['danceability']
        energy += playlist_reponse.json()["audio_features"][i]['energy']
        instrumentalness += playlist_reponse.json()["audio_features"][i]['instrumentalness']
        liveness += playlist_reponse.json()["audio_features"][i]['liveness']
        loudness += playlist_reponse.json()["audio_features"][i]['loudness']
        valence += playlist_reponse.json()["audio_features"][i]['valence']


    '''print('Tempo:',tempo/playlist_length)
    print('Acousticness:',acousticness/playlist_length)
    print('danceability:',danceability/playlist_length)
    print('Energy:',energy/playlist_length)
    print('Instrumentalness:',instrumentalness/playlist_length)
    print('Liveness:',liveness/playlist_length)
    print('Loudness:',loudness/playlist_length)
    print('Valence:',valence/playlist_length)'''
       
top_10()    
play_list_audio_features()    