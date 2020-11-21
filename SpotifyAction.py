import requests
import json
from refresh import Refresh
from secrets import spotify_token, spotify_user_id

class Spotify:

    def __init__(self):
        self.spotify_token = Refresh().refresh()
        self.user_id = spotify_user_id
        self.playlist_uri = ""
        self.playlist_id = ""
        self.getPlaylist()

    def getPlaylist(self):
        try:
            query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.spotify_token)
                }
            )
            response = response.json()["items"]
            exists = False
            for v in response:
                if v["name"] == "Boombox Playlist":
                    print('playlist exists and attached')
                    exists = True
                    self.playlist_uri= v["uri"]
                    self.playlist_id = v["uri"].split(':')[2]
                if not exists:
                    self.create_playlist()
        except:
            self.create_playlist()
    
    def create_playlist(self):
        print('creating new playlist')
        # Create a new playlist
        query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
        
        request_body = json.dumps({
            "name": "Boombox Playlist", "description": "Songs from SMS", "public": True
        })
        response = requests.post(query, data=request_body, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        })
        response_json = response.json()
        self.playlist_uri = response_json["uri"]
        self.playlist_id = response_json["uri"].split(':')[2]
    
    def play_start(self):
        print('play')
        query = "https://api.spotify.com/v1/me/player/play"
        request_body = json.dumps({"context_uri": "{}".format(self.playlist_uri)})
        response = requests.put(query, data=request_body,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )

        #response_json = response.json
        #print(response.json['Responses'])
        #print(response_json['error']['status'])
        #if(playTime == 0): return False
        #if(response.json['Responses'] != '<bound method Response.json of <Response [204]>>'):
            #print("fail")
            #response_json = response.json()
            #if(response_json['error']['status'] == 400 or response_json['error']['status'] == 404):
                #print("error")
                #return False
        #else:
            #return True
        
    def play(self):
        print('play')
        query = "https://api.spotify.com/v1/me/player/play"
        response = requests.put(
            query,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        #print("response from actions_song 2")
        #print(response.json)
        
    def pause(self):
        print('pausing')
        query = "https://api.spotify.com/v1/me/player/pause"
        request_body = json.dumps({"context_uri": "{}".format(self.playlist_uri)})
        response = requests.put(query, data=request_body,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        #print("response from actions_song")
        #print(response.json)
        
    def nextSong(self):
        query = "https://api.spotify.com/v1/me/player/next"
        response = requests.post(query,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        #print("response from skip_to_nextSong")
        #print(response.json)
        
    def prevSong(self):
        query = "https://api.spotify.com/v1/me/player/previous"
        response = requests.post(query,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        #print("response from skip_to_prevSong")
        #print(response.json)
        
    def shuffle(self):
        query = "https://api.spotify.com/v1/me/player"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        response_json = response.json()
        shuffle = response_json["shuffle_state"]
        query = "https://api.spotify.com/v1/me/player/shuffle?state={}".format(
            not shuffle)
        response = requests.put(query,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        #print("play_shuffle")
        #print(response.json)
        
    def repeat(self):
        query = "https://api.spotify.com/v1/me/player"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        response_json = response.json()
        repeat = response_json["repeat_state"]
        if (repeat == "context"):
            repeat = "off"
        else:
            repeat = "context"
        query = "https://api.spotify.com/v1/me/player/repeat?state={}".format(
            repeat)
        response = requests.put(query,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        
    def formatSong(self, txt):
        data = txt.split("::")
        song_name = data[0]
        artist = data[1]
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()
        song = response_json["tracks"]["items"][0]["uri"]
        return song 
    
    def add(self, song):
        song = self.formatSong(song)
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            self.playlist_id, song)
        response = requests.post(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        #print("added song is " + song[0])
        #print(response.json)
    

    def remove(self, song):
        #this removes all of the same song, you could search for a specific song though
        song = self.formatSong(song)
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            self.playlist_id)
        request_body = json.dumps(
            { "tracks": [{"uri": "{}".format(song)}]})
        response = requests.delete(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        
    def clear(self):
        query = "https://api.spotify.com/v1/playlists/{}/followers".format(
            self.playlist_id)
        response = requests.delete(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        self.create_playlist()
