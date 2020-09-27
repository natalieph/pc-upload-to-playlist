# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 17:40:19 2020

@author: Chen Zecharya and Natalie Philip
"""
import eyed3
import spotipy
import spotipy.util as util
import glob



def create_new_playlist(cid, cis, uid, playlist_name, root_dir):       
    #creating token request usings the credenrials
    t2 = util.prompt_for_user_token(username = uid, client_id = cid, client_secret = cis, redirect_uri = "https://open.spotify.com/", scope = "playlist-modify-public")
    sp = spotipy.Spotify(auth=t2)
    
    # Create new playlist
    playlist_info = sp.user_playlist_create(user = uid, name = playlist_name)
    playlist_id = playlist_info["id"]
       
    #using a directory of songs
    root_dir = root_dir.replace("\\", "\\\\")
    root = glob.glob(root_dir + "\\*.mp3")
    
    # format the songs into a list 
    playlist = list()
    for file in root:
        audiofile = eyed3.load(file)
        if audiofile.tag.artist is not None and audiofile.tag.title is not None:
            artist,track = audiofile.tag.artist, audiofile.tag.title
            playlist.append((artist, track))
        elif "-" in file:
            file = file.split("\\")[-1]
            file = file.replace(".mp3", "")
            # file = file.replace(" ", "+")
        
            artist, track = file.split("-")
            playlist.append((artist, track))
        else:
            playlist.append((file.split("\\")[-1], ""))

    print("the following songs were found:")
    for artist,track in playlist:
        print(artist,track)
    print()
    song = None
    tracks = list()
    
    for artist, track in playlist:
        # create new query to search the track
        song = sp.search(q = "artist:{} track:{}".format(artist, track), limit = 1, type = "track")
        for key, value in song.items():
            for k2, v2 in value.items():
                if k2 == "items":
                    for item in v2:
                        for k3, v3 in item.items():
                            if k3 == "id":
                                tracks.append(v3)
                                print("song",artist,track,"added to list")
          #add the tracks to the playlist we created                  
    sp.user_playlist_add_tracks(user = uid, playlist_id = playlist_id, tracks = tracks)
    

def main():
    cid = input("Enter client id:")
    cis = input("Enter client secret:")
    uid = input("Enter user id:")
    playlist_name = input("Enter playlist name:")
    root_dir = input("Enter root dir:")
    create_new_playlist(cid = cid, cis = cis, uid = uid, playlist_name = playlist_name, root_dir = root_dir)
    
if __name__ == "__main__":
    main()


