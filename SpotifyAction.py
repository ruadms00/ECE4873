import requests
import json
import os

class Spotify:

    def initializeVariables(self):
        self.songAdded = False
        self.offset = 0
        self.playlist_uri = ""
        self.playlist_id = ""
        self.deviceId = ""
        self.user_id = ""
        self.spotify_token = ""
        self.refresh_token = ""
        if not self.initializeTokens():
            print('get token failed')
            return False
        if not self.refreshTokens():
            print('refresh token failed')
            return False
        if not self.getUser():
            print('get user failed')
            return False
        if not self.getPlaylist():
            print('get playlist failed')
            return False
        if not self.checkDevice():
            print('check device failed')
            return False
        print('spotify initialized')
        self.initialized = True
        return True

    def initializeTokens(self):
        try:
            with open("secrets.txt", "r") as file:
                print('read')
                lines = file.readlines()
                if len(lines) >= 2:
                    print('enough lines')
                    self.spotify_token = lines[0]
                    self.refresh_token = lines[1]
                else:
                    return False
            return True
        except:
            return False

    def updateTokens(self, access, refresh):
        try:
            with open("secrets.txt", "w+") as file:
                data = access + '\n' + refresh
                file.write(data)
                file.flush()
                os.fsync(file.fileno())
                self.spotify_token = access
                self.refresh_token = refresh
            return True
        except:
            return False

    def getTokens(self, code):
        query = "https://accounts.spotify.com/api/token"
        try:
            response = requests.post(
                query,
                data={"grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": "https://76.17.103.152/ControlSettings.php",
                    "client_id": "712cfaf86d28475db28376353db9e381",
                    "client_secret": "06450ee50aca4453b40fa82468bfaa0e"
                },
                timeout=(1,3)
            )
            return self.updateTokens(response.json()["access_token"], response.json()["refresh_token"])
        
        except:
            print(query)
            print('exception reached')
            return False
        
    def refreshTokens(self):
        query = "https://accounts.spotify.com/api/token"
        try:
            response = requests.post(
                query,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.refresh_token,
                    "client_id": "712cfaf86d28475db28376353db9e381",
                    "client_secret": "06450ee50aca4453b40fa82468bfaa0e"
                },
                timeout=(1,3)
            )
            variables = vars(response)
            if variables['status_code'] == 401:
                spotify.initialized = False
                return False
            elif variables['status_code'] == 200 or variables['status_code'] == 204:
                refresh = self.refresh_token
                try:
                    refresh = response.json()["refresh_token"]
                except:
                    pass
                return self.updateTokens(response.json()["access_token"], refresh)
            else:
                return False
        except:
            print(query)
            print('exception reached')
            return False


    def __init__(self):
        self.initialized = False
        self.initializeVariables()
    
    def getReq(self,req):
        query = "https://api.spotify.com/" + req
        try:
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.spotify_token)
                },
                timeout=(1,3)
            )
            variables = vars(response)
            if variables['status_code'] == 200:
                return response.json()
            elif variables['status_code'] == 204:
                return False
            elif variables['status_code'] == 401:
                success = self.refreshTokens()
                if success:
                    print('tokens failed, updated')
                else:
                    print('tokens failed, not updated')
                return False
            else:
                print(variables['status_code'])
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
                },
                timeout=(1,3)
            )
            return True
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
                },
                timeout=(1,3) 
            )
            return True
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
                },
                timeout=(1,3)
            )
            variables = vars(response)
            if variables['status_code'] == 200:
                return response.json()
            elif variables['status_code'] == 204:
                return False
            elif variables['status_code'] == 401:
                success = self.refreshTokens()
                if success:
                    print('tokens failed, updated')
                else:
                    print('tokens failed, not updated')
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
                    return True
            return True
        return False

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
          
    def getUser(self):
        response = self.getReq("v1/me")
        if response:
            self.user_id = response["id"]
            return True
        else:
            return False
    
    def getPlaylist(self):
        response = self.getReq("v1/users/{}/playlists".format(self.user_id))
        if response:
            items = response["items"]
            for v in items:
                if v["name"] == "Boombox Playlist":
                    self.playlist_uri = v["uri"]
                    self.playlist_id = v["uri"].split(':')[2]
                    return True
            return self.create_playlist()
        else:
            return self.create_playlist()
    
    def create_playlist(self):
        # Create a new playlist
        jsond = json.dumps({"name": "Boombox Playlist", "description": "Boombox Queue", "public": True})
        response = self.postReq("v1/users/{}/playlists".format(self.user_id), jsond)
        print(response)
        if response:
            self.playlist_uri = response["uri"]
            self.playlist_id = self.playlist_uri.split(':')[2]
            return True
        return False
    
    def play_start(self):
        jsond = json.dumps({
            "context_uri":"{}".format(self.playlist_uri),
            "offset":{"position":self.offset}
        })
        if self.deviceId != "":
            response = self.putReq("v1/me/player/play?device_id={}".format(self.deviceId),jsond)
        else:
            response = self.putReq("v1/me/player/play")
        if not response:
            return False
        return True

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
