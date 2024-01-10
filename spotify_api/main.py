import requests

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
artistas_mas_escuchados = 'me/top/artists'

params = {
    'time_range' : "long_term",
    'limit' : 10
}

#response = requests.get(base_url+"artists/"+artist_id, headers=headers, params=params)
response = requests.get(base_url+artistas_mas_escuchados, headers=headers, params=params)

if response:    
    pass
    #print(response.json())
else:
    print(f"Error {response.status_code}")
    print(response.content)

print('URL solicitada:',response.url)
print('Tiempo de respuesta:',response.elapsed)
print('Encoding:',response.encoding)
print('-------------------------------------')


#print(response.json()["items"][9]['name'])
counter = 1 
print('Los 10 artistas más escuchados por el usuario')
for i in response.json()["items"]:
    for clave , valor in i.items():
        if clave == 'name':
            print(counter, ':', valor)
            counter +=1

    