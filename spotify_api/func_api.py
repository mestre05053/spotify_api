import requests
import json 

from collections import Counter
from auth import Auth

class Func_api:

    def __init__(self):
        self.__auth = Auth()
        self.__token = self.__auth.get_token()
        self.__params = {
                    'time_range' : "long_term",
                    'limit' : 10
                    }
        self.__headers = {
                    'Authorization': f'Bearer {self.__token}',
                    "Accept": "application/json"
                    }
        self.__urls = {
            'url_artistas_mas_escuchados'   : 'https://api.spotify.com/v1/me/top/artists',
            'url_canciones_mas_escuchados'  : 'https://api.spotify.com/v1/me/top/tracks',
            'url_image_cover'               : 'https://api.spotify.com/v1/playlists/37i9dQZF1DWWGFQLoP9qlv/images',
            'url_num_followers'             : 'https://api.spotify.com/v1/playlists/37i9dQZF1DWWGFQLoP9qlv',
            'url_get_track_id'              : 'https://api.spotify.com/v1/playlists/37i9dQZF1DWWGFQLoP9qlv/tracks',
            'url_audio_features'            : 'https://api.spotify.com/v1/audio-features',
                }
        
        #### DICT PARA JSON
        self.__artistas_favoritos = {}
        self.__generos_favoritos = {}
        self.__canciones_favoritas = {}
        self.__audio_features = {}
        self.__list_tracks_id = []
        self.__playlist_length = 0

        #funciones en el constructor
        self.__artistas_mas_escuchados()
        self.__canciones_mas_escuchadas()
        self.__image_cover()
        self.__num_followers()
        self.__get_track_id()
        self.__playlist_audio_features()
        self.__export_json()

    def __artistas_mas_escuchados(self):
        
        response = requests.get(self.__urls['url_artistas_mas_escuchados'], headers=self.__headers, params=self.__params)
        counter = 0
        list_genres = []
        print('Los 10 artistas más escuchados por el usuario')
        for i in response.json()["items"]:
            for clave , valor in i.items():
                if clave == 'name':
                    self.__artistas_favoritos[counter] = valor
                    print(counter, ':', valor)
                if clave == 'genres':
                    for i in valor:
                        list_genres.append(i)
                    counter_list_genres = Counter(list_genres).most_common(5)
                    counter +=1
        print('-------------------------------------')
        print('Los 5 géneros musicales favoritos')                              
        for index, value in enumerate(counter_list_genres):
             self.__generos_favoritos[index] = value[0]
             print(index + 1, value[0])

    def __canciones_mas_escuchadas(self):

        response = requests.get(self.__urls['url_canciones_mas_escuchados'], headers=self.__headers, params=self.__params)

        for i in range(self.__params['limit']):
            track_name_dict = response.json()["items"][i]["name"]
            self.__canciones_favoritas[track_name_dict] = []
            artist_names = response.json()["items"][i]["album"]["artists"]
            for i in artist_names:
                for track_name, artist_name in i.items():
                    if track_name == 'name':
                        self.__canciones_favoritas[track_name_dict].append(artist_name)
        print('Las 10 canciones más escuchadas por el usuario y sus respectivos artistas')
        for clave, valor in self.__canciones_favoritas.items():
            print(clave, ':', str(valor)[1:-1].replace("'", ""))

    def __image_cover(self):

        response = requests.get(self.__urls['url_image_cover'], headers=self.__headers, params=self.__params)
        print('-------------------------------------')
        print('Descargando cover de la URL:', response.json()[0]["url"])
        image_data = requests.get(response.json()[0]["url"]).content 
        image = open('playlist_cover.jpg','wb')
        image.write(image_data) 
        image.close() 
    
    def __num_followers(self):

        response = requests.get(self.__urls['url_num_followers'], headers=self.__headers, params=self.__params)
        print('Número de followers:', response.json()["followers"]["total"])
        self.__audio_features['Followers'] = response.json()["followers"]["total"]
        print('-------------------------------------')

    def __get_track_id(self):

        response = requests.get(self.__urls['url_get_track_id'], headers=self.__headers,)
        self.__playlist_length =  len(response.json()["items"])    
        for i in range(self.__playlist_length):
            tracks_id = response.json()["items"][i]["track"]["id"]
            self.__list_tracks_id.append(tracks_id)
            ## unpacking the list in the variable
        self.__list_tracks_id = "ids="+",".join(self.__list_tracks_id)
       
    def __playlist_audio_features(self):
        print('Valor medio de los siguientes parámetros de todas las canciones')
        response = requests.get(self.__urls['url_audio_features'], headers=self.__headers,params=self.__list_tracks_id)
        list_audio_features = ['tempo','acousticness','danceability','energy','instrumentalness','liveness','loudness','valence']
        result = 0       
        for feature in list_audio_features:
            for i in range(self.__playlist_length):
                result += response.json()["audio_features"][i][feature]
            result = result / self.__playlist_length
            print(feature,':', result )
            self.__audio_features[feature] = result
            result = 0

    def __export_json(self):
        
        with open("spotify_api.json", "w",encoding='utf-8') as outfile:
            json.dump([self.__artistas_favoritos,
                       self.__generos_favoritos,
                       self.__canciones_favoritas,
                       self.__audio_features,
                       ], 
                      outfile, indent = 4,ensure_ascii=False) 

Func_api()
