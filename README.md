### Pasos para el desarrollo

1. **Instalación de dependencias**:
   - Instala Flask y las bibliotecas necesarias con `pip`:
     ```bash
     pip install Flask requests spotipy
     ```

2. **Configuración de la API de Spotify**:
   - Regístrate en [Spotify for Developers](https://developer.spotify.com/dashboard/applications) y crea una aplicación para obtener tu `client_id` y `client_secret`.

3. **Estructura de archivos**:

   ```
   /spotify-web-app
   ├── app.py  # Archivo principal de la aplicación Flask
   ├── templates/
   │   └── index.html  # Página principal HTML
   └── static/
       └── style.css  # Estilos para la página web
   ```


### Cómo ejecutar la aplicación

1. Asegúrate de que las dependencias estén instaladas (`Flask`, `requests`, `spotipy`).
2. Rellena tu `client_id` y `client_secret` en `app.py`.
3. Ejecuta la aplicación:
   ```bash
   python app.py
   ```
4. Abre tu navegador en `http://127.0.0.1:5000` para ver la página de búsqueda de canciones.

### Explicación

- El archivo `app.py` maneja la lógica del servidor usando Flask. Cuando el usuario envía una búsqueda, se realiza una solicitud a la API de Spotify para buscar canciones que coincidan con la consulta.
- La página `index.html` contiene el formulario de búsqueda y muestra los resultados, incluidos el nombre de la canción, el artista, el álbum, y una vista previa si está disponible.
- El archivo `style.css` añade algunos estilos básicos para hacer la página más atractiva.
