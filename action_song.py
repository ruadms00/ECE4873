import requests
import json
playlist_uri = ""
class Action:

    def __init__(self, id, uri, token):
        self.playlist_id = id
        self.playlist_uri = uri
        self.spotify_token = token


    def play_1(self):
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
        
    def play_2(self):
        query = "https://api.spotify.com/v1/me/player/play"
        response = requests.put(
            query,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)

            }  
        )
        print("response from actions_song 222222")
        print(response.json)
        
    def pause(self):
        query = "https://api.spotify.com/v1/me/player/pause"
        request_body = json.dumps({"context_uri": "{}".format(self.playlist_uri)})
        response = requests.put(query, data=request_body,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        print("response from actions_song")
        print(response.json)
        
    def skip_to_nextSong(self):
        query = "https://api.spotify.com/v1/me/player/next"
        response = requests.post(query,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        print("response from skip_to_nextSong")
        print(response.json)
        
    def skip_to_prevSong(self):
        query = "https://api.spotify.com/v1/me/player/previous"
        response = requests.post(query,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        print("response from skip_to_prevSong")
        print(response.json)
        
    def play_shuffle(self, bool):
        query = "https://api.spotify.com/v1/me/player/shuffle?state={}".format(
            bool)
        response = requests.put(query,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        print("play_shuffle")
        print(response.json)
        
    def play_repeat(self):
        query = "https://api.spotify.com/v1/me/player/repeat?state=context"
        response = requests.put(query,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        print("play_in_playlist")
        #print(response.json())
        
        
