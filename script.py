import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
import os
import re
import yt_dlp
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:8888/callback'

DESKTOP_PATH = os.path.expanduser("~/Desktop")


def clean_file(name:str) -> str:
    #Removes characters illegal in MacOS File Name
    return re.sub(r'[\/\:\*\?"<>\|]', "", name).strip()


def get_tracks(url: str) -> list[dict]:
    #Returns the list of {title, artist} dicts from playlist
    auth_manager = SpotifyClientCredentials(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
    )
    sp = spotipy.Spotify(auth_manager = auth_manager)
    match = re.search(r'playlist/([A-Za-z0-9]+)', url)
    if not match:
        print("Could not parse ID")
        return []
    playlist_id = match.group(1) #splits url from url -> readable playlist ID
    #Example: https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=abc123xyz. --> 37i9dQZF1DXcBWIGoYBM5M
    #Uses splitting techniques
    print(f" Extracted ID: {playlist_id}")
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

        results = sp.next(results) if results["next"] else None
    
    return tracks

def progress_hook(d):
    if d["status"] == "downloading":
        print(f" Downloading... {d.get('_percent_str', '').strip()}",end="\r")
    elif d["status"] =="finished":
        print(f" Download complete, converting to mp3")


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
        "progress_hooks": [progress_hook],
    }
    print(f" Searching Youtube for {search_query}")
    try: 
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f" Starting download...")
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
       artist = track["artist"]
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