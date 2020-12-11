import requests
import json
from refresh import Refresh
from secrets import spotify_token, spotify_user_id

class Spotify:

    def __init__(self):
        self.spotify_token = Refresh().refresh()
        self.user_id = spotify_user_id
        self.songAdded = False
        self.offset = 0
        self.playlist_uri = ""
        self.playlist_id = ""
        self.deviceId = ""
        self.getPlaylist()
        self.checkDevice()
        self.play_start()
    
    
    def getReq(self,req):
        query = "https://api.spotify.com/" + req
        try:
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.spotify_token)
                }
            )
            variables = vars(response)
            if(variables['status_code'] == 200):
                return response.json()
            elif(variables['status_code'] == 204):
                print(query)
                print('status fail')
                return False
        except:
            print(query)
            print('exception reached')
            return False
        
    def putReq(self, req, body = None):
        query = "https://api.spotify.com/" + req
        try:
            response = requests.put(
                query,
                data=body,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.spotify_token)
                }  
            )
        except:
            print(query)
            print('exception reached')
            return False
    
    def delReq(self, req, body = None):
        query = "https://api.spotify.com/" + req
        try:
            response = requests.delete(
                query,
                data=body,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.spotify_token)
                }  
            )
        except:
            print(query)
            print(body)
            print('exception reached')
            return False
        
    def postReq(self, req, body = None):
        query = "https://api.spotify.com/" + req
        try:
            response = requests.post(
                query,
                data=body,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.spotify_token)
                }  
            )
        except:
            print(query)
            print('exception reached')
            return False
        
    def checkDevice(self):
        response = self.getReq("v1/me/player/devices")
        if response:
            devices = response["devices"]
            device = 0
            for i in devices:
                if i["name"][0:10] == "raspotify ":
                    device = i["id"]
                    self.deviceId = device
                    if (not i["is_active"]):
                        self.offset = 0
                        self.play_start()
                    break

    def getSongInfo(self):
        response = self.getReq("v1/me/player/currently-playing")
        return response

    def getArt(self):
        response = self.getReq("v1/me/player/currently-playing")
        if response:
            return response['item']['album']['images'][1]['url']
        else:
            return False
        
    def isPlaying(self):
        response = self.getReq("v1/me/player/currently-playing")
        if response:
            return response['is_playing']
        else:
            return False
        
    def getName(self):
        response = self.getReq("v1/me/player/currently-playing")
        if response:
            return response['item']['name']
        else:
            return False
        
    def getSongUri(self):
        response = self.getReq("v1/me/player/currently-playing")
        if response:
            return response['item']['uri']
        else:
            return False
        
    def getArtist(self):
        response = self.getReq("v1/me/player/currently-playing")
        if response:
            return response['item']['artists'][0]['name']
        else:
            return False
    
    def getLength(self):
        response = self.getReq("v1/me/player/currently-playing")
        if response:
            return response['item']['duration_ms'] // 1000
        else:
            return False
            
    def getQueue(self):
        response = self.getReq("v1/playlists/{}/tracks".format(self.playlist_id))
        items = []
        if response:
            items = response["items"]
        else:
            return []
        queue = []
        for i in items:
            song = i["track"]["name"]
            artist = i["track"]["artists"][0]["name"]
            queue.append(song + "::" + artist)
        return queue
        
    def getPlaylist(self):
        response = self.getReq("v1/users/{}/playlists".format(spotify_user_id))
        if response:
            items = response["items"]
            exists = False
            for v in items:
                if v["name"] == "Boombox Playlist":
                    exists = True
                    self.playlist_uri = v["uri"]
                    self.playlist_id = v["uri"].split(':')[2]
            if not exists:
                self.create_playlist()
        else:
            self.create_playlist()
    
    def create_playlist(self):
        # Create a new playlist
        jsond = json.dumps({"name": "Boombox Playlist", "description": "Boombox Queue", "public": True})
        response = self.postReq("v1/users/{}/playlists".format(spotify_user_id), jsond)
        if response:
            self.playlist_uri = response_json["uri"]
            self.playlist_id = response_json["uri"].split(':')[2]
        else:
            return False
    
    def play_start(self):
        jsond = json.dumps({
            "context_uri":"{}".format(self.playlist_uri),
            "offset":{"position":self.offset}
        })
        response = self.putReq("v1/me/player/play?device_id={}".format(self.deviceId),jsond)

    def play(self):
        self.putReq("v1/me/player/play")
        
    def pause(self):
        self.putReq("v1/me/player/pause")
        
    def nextSong(self):
        self.postReq("v1/me/player/next")
        
    def prevSong(self):
        self.postReq("v1/me/player/previous")
        
    def shuffle(self):
        response = self.getReq("v1/me/player")
        shuffle = response["shuffle_state"]
        self.putReq("v1/me/player/shuffle?state={}".format(not shuffle))

    def repeat(self):
        response = self.getReq("v1/me/player")
        repeat = response["repeat_state"]
        if (repeat == "context"):
            repeat = "off"
        else:
            repeat = "context"
            self.putReq("v1/me/player/repeat?state={}".format(repeat))
        
    def formatSong(self, txt):
        data = txt.split("::")
        song_name = data[0]
        artist = data[1]
        response = self.getReq("v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        ))
        if response:
            items = response["tracks"]["items"]
            if len(items) == 0:
                return False
            return items[0]["uri"]
        else:
            return False
    
    def addQueue(self, song):
        self.postReq("v1/me/player/queue?uri={}".format(song))
        
    def add(self, song):
        song = self.formatSong(song)
        self.postReq("v1/playlists/{}/tracks?uris={}".format(self.playlist_id, song)) 
        self.songAdded = True
    

    def remove(self, song):
        #this removes all of the same song, you could search for a specific song though
        song = self.formatSong(song)
        jsond = json.dumps(
            { "tracks": [{"uri": "{}".format(song)}]})
        self.delReq("v1/playlists/{}/tracks".format(self.playlist_id), jsond)
        
    def clear(self):
        self.delReq("v1/playlists/{}/followers".format(self.playlist_id))
        self.create_playlist()

    def updateLocation(self):
        song_uri = self.getSongUri()
        if song_uri == False:
            return False
        response = self.getReq("v1/playlists/{}/tracks".format(self.playlist_id))
        items = False
        if response:
            items = response["items"]
        else:
            return False
        j = 0
        for i in items:
            song = i["track"]["uri"]
            if song == song_uri:
                if j == 0 and self.offset > 0:
                    if self.songAdded:
                        self.offset = self.offset + 1
                        self.play_start()
                        self.songAdded = False
                elif self.offset != j:
                    self.offset = j
                break
            j = j + 1
