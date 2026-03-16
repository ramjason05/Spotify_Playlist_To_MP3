This is a spotify playlist URL converter to MP3 using yu_dlp youtube parser and mp3 downloader
This would be using Spotipy to link to your spotify ID and Secret which you should create a ".env" file like my example file has,
to link your specific IDs, which you can find at https://developer.spotify.com/

The Steps to Use the Downloader:
  1.Copy SSH and copy github repository
  2.Create your own virtual environment in your terminal: -python3 -m venv venv
  3.Activate your virtual enviorment:
  -Windows Command Prompt (cmd.exe): myenv\Scripts\activate.bat -WindowsPowerShell: .\myenv\Scripts\Activate.ps1 -macOS and Linux (Bash/Zsh): source myenv/bin/activate -VS Code: Open the Command Palette ((Ctrl+Shift+P) or (Cmd+Shift+P)), select "Python: Select Interpreter," and choose the environment within your project folder -Conda Environment: conda activate <env_name>

In the terminal, install the dependencies through the requirements.txt -pip3 install -r requirements.txt
You also have to install ffmeg through brew seperatly; use the line 'brew install ffmpeg'

-Now you can run the program
