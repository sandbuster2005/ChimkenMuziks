# ChimkenMuziks
A humanmade AI free MP3 player

this is a cli player which plan to be easily~ish usable , highly configurable
and good looking

dependancy:
- vlc
- python 
- PIL

currently its allow you to :
- select a  main folder (and to change it)
- load specific sub-folder
- edit command to your liking
- rename / move / remove songs
- play mp3,waw,m4a,flac,,ogg,midi*
- play in loop,order,random
- forwarding , backwarding
- go to previous / next song
- load last played song when starting the player
- ay song via command
- search for song
- favorites
- create and edit playlists
- show historic of current session
- show file image or image of your chosing (random or not) if not  
- search on youtube and download*
- enter youtube link and download*
- see your mosts played song
- set a configurable timer
- additionnal parameters 


*additionnal dependancy required

to download from youtube:
- yt-dlp

for .midi:
- fluidsynth

for easier folder selection:
- xplr

for alsaaudio (use global volume instead of vlc instance):
- alsaaudio
- on ARCH alsa-lib
- on UNBUNTU libasound2-dev

windows version is in the making but cli is not really adapted to windows
	
there are still bug every now and then but hey it work 

![exemple display during a song](/example.png)
