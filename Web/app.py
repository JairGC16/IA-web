from flask import Flask, render_template, request, jsonify
import requests
import base64

app = Flask(__name__)

client_id = 'b56a335c7ac345e2b272f55a6793a0ab'
client_secret = 'd10d4bb8e3e64e84a3abdb79c8f4466a'

def get_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    headers = {}
    data = {}

    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode())

    headers['Authorization'] = f"Basic {client_creds_b64.decode()}"
    data['grant_type'] = 'client_credentials'

    response = requests.post(auth_url, headers=headers, data=data)
    token_response_data = response.json()
    return token_response_data['access_token']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    if query:
        token = get_token()
        search_url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=10"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(search_url, headers=headers)
        search_data = response.json()

        tracks = []
        if 'tracks' in search_data:
            for item in search_data['tracks']['items']:
                track_info = {
                    'name': item['name'],
                    'artist': ', '.join([artist['name'] for artist in item['artists']]),
                    'album': item['album']['name'],
                    'preview_url': item['preview_url'],
                    'image': item['album']['images'][0]['url'] if item['album']['images'] else ''
                }
                tracks.append(track_info)
        return jsonify(tracks)
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
