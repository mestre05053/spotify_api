# Actividad 02

Peso - 50% del PortFolio

- Primera Convocatoria 19/01/2024

Spotify es un servicio de música, donde se pueden escuchar millones de canciones de manera gratuita (existe una suscripción de pago con funcionalidades extra). El objetivo de esta actividad es recoger cierta información de los gustos musicales de cada usuario de la plataforma. Para ello, si aún no se tiene un perfil en Spotify, se recomienda crearse uno y escuchar algo de música mientras se desarrolla la actividad para generar los datos necesarios en la plataforma.

Se puede hacer uso de la API Web de Spotify (https://developer.spotify.com/documentation/web-api/) directamente a través de la librería requests, o se puede hacer uso de alguna librería de Python que facilite la conexión (https://pypi.org/project/spotipy/).

El primer paso es conseguir autenticarse contra la plataforma de Spotify con permisos completos para acceder al perfil del usuario a través de OAuth, y que se puedan consultar los datos requeridos en cada apartado. Para facilitar dicha tarea se provee el código de la clase Auth, que tiene dos métodos públicos, el primero *generate_token*, que se puede usar para crear un nuevo token de conexión (para ello habrá que modificar las variables de clase *client_id* y *client_secret*, que deberían corresponder con las de vuestra aplicación). El segundo método es *get_token*, que hace uso de un token previamente generado y almacenado para su uso posterior, en caso de que ese token haya caducado, intenta regenerarlo.

El script contenido en *main.py* hace uso de dicha clase Auth para conectarse a la API de Spotify y realizar una búsqueda.

Se piden los siguientes datos:

- Los 10 artistas más escuchados por el usuario
- A través de esos 10 artistas, obtener una lista de los 5 géneros musicales favoritos de dicho usuario
- Las 10 canciones más escuchadas por el usuario y sus respectivos artistas
- Sobre la playlist https://open.spotify.com/playlist/37i9dQZF1DWWGFQLoP9qlv
  - Guardar en disco la portada de dicha Playlist
  - Obtener el número de followers
  - Obtener el valor medio de los siguientes parámetros de todas sus canciones
    - Tempo (BPM)
    - Acousticness
    - Danceability
    - Energy
    - Instrumentalness
    - Liveness
    - Loudness
    - Valence

Todos estos datos deberán guardarse en un fichero o ficheros (CSV, Json, u otro formato adecuado) para su posible posterior análisis y representación gráfica.

Al crear vuestra aplicación en Spotify en modo desarrollo, se tiene que añadir el email de la cuenta de Spotify con la que se vaya a probar su funcionalidad, en ese caso, se recomienda que se autorice la cuenta del profesor (ivan.fuertes@professor.universidadviu.com) para que se pueda ejecutar la aplicación correctamente a la hora de evaluarla.

Si se va a usar la clase Auth adjunta, en la web de la API de Spotify, en la sección Settings, hay que añadir en la sección "Redirect URIs" de vuestra app, la siguiente dirección local de vuestra maquina "http://localhost:8080"
