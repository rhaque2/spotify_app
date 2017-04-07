import spotipy
import spotipy.util as util
import base64
import requests
import json
import time
import urlparse

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from json import JSONEncoder
from urlparse import urlparse

client_id = '5d1b3d42cd2a49f08f6a64d7f5f781de';
client_secret = 'bd1e35485ae74b3386a20b54df6a56e2';

url = 'https://accounts.spotify.com/authorize'
data = {'client_id':'5d1b3d42cd2a49f08f6a64d7f5f781de',
        'response_type':'code',
        'redirect_uri':'https://www.spotify.com/us/',
        'scope':'user-library-read'
        }
get = requests.get(url, params = data);
driver = webdriver.Chrome('C:\Users\Ruhul\Web Drivers\chromedriver.exe')
driver.get(get.url);


while True:
    if "code=" in driver.current_url:
        print (driver.current_url);
        parsed_url = urlparse(driver.current_url);
        query = parsed_url.query;
        code = query[5:];
        print code
        payload = {'grant_type':'authorization_code',
        'code':code,
        'redirect_uri':'https://www.spotify.com/us/'
        }
        headers = {'Authorization' : 'Basic '+base64.standard_b64encode(client_id + ':' + client_secret)}
        post = requests.post('https://accounts.spotify.com/api/token', data = payload, headers=headers)
        print post
        print ''
        print ''
        content = post.content    # in a string
        print type(content)
        dictionary = json.loads(content)  # converts to dict
        print type(dictionary)
        token = dictionary['access_token'] # store the access_token
        refresh_token = dictionary['refresh_token']
        print token
        print refresh_token
        print ''  # After here we start applying the token
        print ''
        values = {'grant_type':'refresh_token',
        'refresh_token':refresh_token
        }
        headers = {'Authorization' : 'Basic '+base64.standard_b64encode(client_id + ':' + client_secret)}
        post2 = requests.post('https://accounts.spotify.com/api/token', data = values, headers=headers)
        print post2
        break
else:
        time.sleep(5)

username='tallentmusic555' #user username 
#email='tallentmusic55@gmail.com' # user email
#password='tallentmusic555' # user password


def show_tracks(tracks): # will print track names when called
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print "   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name'])


if token: #uses token to look at contents of user's playlists
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            print
            print playlist['name']
            print '  total tracks', playlist['tracks']['total']
            results = sp.user_playlist(username, playlist['id'],
                fields="tracks,next")
            tracks = results['tracks']
            show_tracks(tracks)
            while tracks['next']:
                tracks = sp.next(tracks)
                show_tracks(tracks)
        else:
            print "Can't get token for", username

driver.quit()

