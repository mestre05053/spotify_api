import requests

from auth import Auth

class Response():

    def __init__(self):
        self.__base_url = 'https://api.spotify.com/v1/'
        self.__url_top_10 = 'me/top/artists'
        
        self.__auth = Auth()
        self.token = auth.get_token()
        self.__headers = {
            'Authorization': f'Bearer {token}',
            "Accept": "application/json"
            }
        self.__params = {
            'time_range' : "long_term",
            'limit' : 10
            }
    
    def data(self, base, headers, params):
        if response:
            pass
            #print(response.json())
        else:
            print(f"Error {response.status_code}")
            print(response.content)

    def top_10(self):

        response = requests.get(self.__base_url+self.__url_top_10, self.__headers,self.__params)
        print('URL solicitada:',response.url)
        print('Tiempo de respuesta:',response.elapsed)
        print('Encoding:',response.encoding)
        print('-------------------------------------')

        counter = 1 
        print('Los 10 artistas más escuchados por el usuario')
        for i in response.json()["items"]:
            for clave , valor in i.items():
                if clave == 'name':
                    print(counter, ':', valor)
                    counter +=1

test = Response()
test.top_10()