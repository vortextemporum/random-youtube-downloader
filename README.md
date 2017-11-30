# youtuberandomdownloader.py

Hi everyone!

This is my first program made with python. I just started learning Python (and it's my first language), so if you have any suggestions to the code, please help me make this better!

I worked on this program because I want to use youtube videos in my ongoing art projects.

It's also my first time using git, so if you see me screwing up with the pull requests and other things, please send me an email! 

With this small program, you can get urls of up to 200 random videos from youtube (you can change the limit in the code easily) and download them. You can choose between 4 languages (english, turkish, german, japanese, or all of them), or you can type your own keyword to get the videos.


### Usage:

* Add your API key to apikey.txt in the main directory (first, if you don't have, get your own API token from Google.)
* You should have youtube_dl module installed. (run "pip install youtube_dl")
* Also you may need to install youtube-dl, ffmpeg on your computer.
* Run the script with python3.
* Follow the steps.
* All video infos will be printed as a json file to the "json" subfolder, and videos will be downloaded to "/output/yourjsonname" folder.


### Things to add:

* More download options (right now it's only 192 kbps mp3 only)
* Handling errors in downloads section.
* Different languages and keyword collections
* Maybe using online apis to get random search keywords instead of using txt files.
* Changing the duration in json to minutes:seconds format.
* Adding other video streaming services (Vimeo, Pornhub etc.)
* Playlist search - download.
* I'm also planning to add a audio/video analysis and trimming tool. But maybe I should do them as separate programs.

### The things that I'm not very happy with:

* It seems like with Google's API I can't search for least watched videos, and the search results are not completely random, it usually finds the most popular result. If you know any ways to dig deeper on Youtube, please contact me.

