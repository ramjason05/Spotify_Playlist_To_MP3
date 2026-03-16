import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
import os
import re
import yt_dlp
from dotenv import load_dotenv
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = 'http://127.0.0.1:8080/callback'

DESKTOP_PATH = os.pathfinder.expanduser("-/Desktop")


def clean_file(name:str) -> str:
    #Removes characters illegal in MacOS File Name
    return re.sub(r'[\/\:\*\?"<>\|]', "", name).strip()


def get_tracks(url: str) -> list[dict]:
    #Returns the list of {title, artist} dicts from playlist
    auth_manager = SpotifyClientCredentials(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
    )
    sp = spotipy.Spotipy(auth_manager = auth_manager)

    playlist_id = url.split("/playlist")[1].split("?")[0] #splits url from url -> readable playlist ID
    #Example: https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=abc123xyz. --> 37i9dQZF1DXcBWIGoYBM5M
    #Uses splitting techniques
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    while results:
        for item in results["items"]:
            track = item.get("track")
            if not track:
                continue
            title = track["name"]
            artist = track["artists"][0]["name"]
            tracks.append({"title":title,"artist":artist})
    
    return tracks


def search_query(title:str, artist:str) -> str:
    #searches on youtube for the clean/official videos to scrape
    return f"{title} - {artist} Official Clean"

def download_as_mp3(search_query:str, output_dir:str, file:str) -> bool:
    #True on success / False on failure
    output_template = os.path.join(output_dir, f"{file}.%(ext)s") #.%(ext)s -> placeholder for type of folder
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template, #directory that its going to be placed in
        "noplaylist": True, #if url leads to playlist, only grab video one
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192", #192 kbps for quality of audio file
        }],
        "default_search": "ytsearch1", # Only grabs the first result, should change possibly
        "quiet": True,
        "no_warnings": True,
    }
    try: 
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([search_query])
        return True
    except Exception as e:
        print(f"Failure to Download due to {e}")
        return False



def main():
   U_P = input("Paste your playlist URL here --> ").strip()

   print(f"\n Fetching tracks from spotify...")
   tracks = get_tracks(U_P)
   print(f"Found {len(tracks)} trakcs.\n")

   #Creating folder on desktop named after the playlist ID
   playlist_id = U_P.split("/playlist/")[1].split("?")[0][:8]
   output_folder = os.path.join(DESKTOP_PATH, f"Playlist_{playlist_id}")
   os.makedirs(output_folder, exist_ok=True) #Creating folder / exist_ok = its okay if file alr exists, still make it
   print(f"Created {output_folder} on your desktop\n")

   success = 0
   fails = 0

   for i, track in enumerate(tracks, start=1):
       title = track["title"]
       artist = track["artists"]
       print(f"[{i}/{len(tracks)}] {artist} - {title}")
       query = search_query(title, artist)
       filename = clean_file(f"{artist} - {title}")

       ok = download_as_mp3(query, output_folder, filename)

       if ok:
           print(f" Saved as {filename}.mp3")
           success += 1
       else:
           fails += 1
       print(f"\n Done! {success} downloaded, and {fails} failed")
       print(f"Files are in: {output_folder}")


if __name__ == "__main__":
    main() 