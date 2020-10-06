import json
import requests
import time
import threading
from action_song import Action
from refresh import Refresh
# from exceptions import ResponseException
from secrets import spotify_token, spotify_user_id
# , discover_weekly_id
offset = 1
class CreatePlaylist:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = ""
        self.tracks = ""
        self.playlist_uri = ""
        self.playlist_id = ""

    def control_start_playlist(self):
        print("control_start_playlist executed")
        file = open("/Users/kyeomeunjang/Desktop/Spotify/start.txt", "r+")  
        read = file.readline()
        file.close()
        file = open("/Users/kyeomeunjang/Desktop/Spotify/start.txt", "w+")  
        file.write("NULL")
        file.close()
        return read
    
    def get_status(self):
        print("get_status")
        file = open("/Users/kyeomeunjang/Desktop/Spotify/status.txt", "r+")  
        read = file.readline()
        file.close()
        return read
    
    def create_playlist(self):
        # Create a new playlist
        print("Trying to create playlist...")
        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)
        request_body = json.dumps({
            "name": "Kyeomeun's Playlist", "description": "Songs from SMS", "public": True
        })
        response = requests.post(query, data=request_body, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        })
        response_json = response.json()
        self.playlist_id = response_json["id"]
        self.playlist_uri = response_json["uri"]
    

    def get_spotify_uri(self, song_name, artist):
        "Search For the Song"
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
        songs = response_json["tracks"]["items"]

        # only use the first song
        uri = songs[0]["uri"]
        return uri
    
    def get_txt_songs(self):
    # "grab the songs in txt files."
        file = open("/Users/kyeomeunjang/Desktop/Spotify/list.txt", "r+")  
        lines = file.readlines()
        firstline = lines[0]
        del lines[0]
        file.close()
        file = open("/Users/kyeomeunjang/Desktop/Spotify/list.txt", "w+")  
        for line in lines:
            file.write(line)
        file.close()
        
        data = firstline.split(" - ")
        song_name = data[0]
        artist = data[1]

        song = self.get_spotify_uri(song_name, artist)
        print(song_name + " + "+ artist)
        return song 
    
    # read a file for 'remove song'
    def get_txt_songs_2(self):
    # "grab the songs in txt files."
        file = open("/Users/kyeomeunjang/Desktop/Spotify/remove.txt", "r+")  
        lines = file.readlines()
        firstline = lines[0]
        del lines[0]
        file.close()
        file = open("/Users/kyeomeunjang/Desktop/Spotify/remove.txt", "w+")  
        for line in lines:
            file.write(line)
        file.close()
        
        data = firstline.split(" - ")
        song_name = data[0]
        artist = data[1]

        song = self.get_spotify_uri(song_name, artist)
        print(song_name + " + "+ artist)
        return song 
       
    def add_song_to_playlist(self):
        song = self.get_txt_songs()
        
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            self.playlist_id, song)
        response = requests.post(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        print("added song is " + song[0])
        print(response.json)
    
    def remove_song_from_playlist(self):
        song_2 = self.get_txt_songs_2()
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            self.playlist_id)
        request_body = json.dumps(
            { "tracks": [{"uri": "{}".format(song_2)}]})
        response = requests.delete(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        print("removed song is " )
        print(response.json)
        
    def call_refresh(self):
        print("refresh")
        refreshCaller = Refresh()
        self.spotify_token = refreshCaller.refresh()
        
    def get_device(self):
        query = "https://api.spotify.com/v1/me/player/devices"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        response_json = response.json()
        print(response_json["devices"])
    def get_song_info(self):
        query = "https://api.spotify.com/v1/me/player/currently-playing"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }  
        )
        response_json = response.json() 
        # Album 
        print(response_json["item"]["name"])
        # Artist
        artist_info = response_json["item"]["artists"]
        print(artist_info[0]["name"])
        # print(response.json())
                
if __name__ == '__main__':
    cp = CreatePlaylist()
    cp.call_refresh()
    cp.get_device()
    while(1):
        time.sleep(3)
        start = cp.control_start_playlist()
        if(start == "start"):
            cp.create_playlist()
           
        elif(start != "start"):
            a_song = Action(cp.playlist_id, cp.playlist_uri, cp.spotify_token)
            status = cp.get_status()
            if(status == 'add'): cp.add_song_to_playlist()
            elif(status == 'play'): 
                if(offset == 1):
                     a_song.play_1()
                     offset = 0
                elif(offset == 0):
                     a_song.play_2()
                
            elif(status == 'pause'): a_song.pause()
            elif(status == 'next'): a_song.skip_to_nextSong()
            elif(status == 'prev'): a_song.skip_to_prevSong()
            elif(status == 'remove'): cp.remove_song_from_playlist()
            elif(status == 'info'): cp.get_song_info()
            elif(status == 'shuffle_on'): a_song.play_shuffle("true")
            elif(status == 'shuffle_off'): a_song.play_shuffle("false")
