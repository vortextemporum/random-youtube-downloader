#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime
import random
import urllib.request
import string
import json
import urllib.parse
import os
import time
import youtube_dl

def Main():    
    #keyword select
    print('How would you like to search for videos?')
    print('1. Use english words')
    print('2. Use turkish words')
    print('3. Use german words')
    print('4. Use japanese words')
    print('5. Use all languages listed above')
    print('6. Type your own keyword')
    
    while True:
        queryChoice = input('Select: ')
        if queryChoice == "1":
            print('Imma gonna search random english words!')
            keyword = "English"
            break
        elif queryChoice == "2":
            print('Imma gonna search random turkish words!')
            keyword = "Turkish"
            break
        elif queryChoice == "3":
            print('Imma gonna search random german words!')
            keyword = "German"
            break
        elif queryChoice == "4":
            print('Imma gonna search random japanese words!')
            keyword = "Japanese"
            break
        elif queryChoice == "5":
            print('Imma gonna search random words from all languages I have!')
            keyword = "Random"
            break
        elif queryChoice == "6":
            print('So what do you want to search for?')
            keyword = input("Your keyword: ")
            break
        else:
            print('Dude... Please... Select... Something... Between... 1-6')
    print("You chose: {}".format(keyword))
    #videoAmount select
    print("----------------------------")
    print('How many videos would you like to get? Max 200')
    while True:
        userChoice = int(input("Amount: "))
        if userChoice in range(1,201):
            print('{} videos then!'.format(userChoice))
            videoAmount = userChoice
            break
        else:
            print("Please write something between 1 and 200.")
    print('Video amount is {}'.format(videoAmount))
    print("----------------------------")

    #videoDuration select
    print('Do you have any preference for duration?')
    print('1. Short')
    print('2. Medium')
    print('3. Long')
    print('4. Naah, just give me random videos!')
    
    while True:
        userChoice = int(input('Duration: '))
        if userChoice == 1:
            videoDuration = "short"
            break
        elif userChoice == 2:
            videoDuration = "medium"
            break
        elif userChoice == 3:
            videoDuration = "long"
            break
        elif userChoice == 4:
            videoDuration = "any"
            break
        else:
            print('Aaaaaargh, please choose 1, 2, 3 or 4. PLEASE.')

    #Order by
    print("You chose {}".format(videoDuration))
    print("----------------------------")
    print("Order by?")
    print("1. Relevance")
    print("2. Date")
    print("3. Rating")
    print("4. Title")
    print("5. View Count (highest to lowest)")

    
   
    while True:
        userChoice = input("Select: ")
        if userChoice == "1":
            orderBy = "relevance"
            break
        elif userChoice == "2":
            orderBy = "date"
            break
        elif userChoice == "3":
            orderBy = "rating"
            break
        elif userChoice == "4":
            orderBy = "title"
            break
        elif userChoice == "5":
            orderBy = "viewCount"
        else:
            print("I don't have to tell you what to do...")

    
    print("You chose {}".format(orderBy))        
    print("----------------------------")
    print("Language/Keyword: {}".format(keyword))
    print("Video Amount: {}".format(videoAmount))
    print("Durations of Videos: {}".format(videoDuration))
    print("Order by: {}".format(orderBy))
    print('Are you sure with this setting? Y/N')
    print('Warning: If you choose No, you are going to turn back to the beginning.')
    print("----------------------------")

    yesorno = input("Y or N: ").lower()
    
    if yesorno.startswith("y"):
        ytfetch(queryChoice,videoAmount,videoDuration,keyword,orderBy)
    else:
        Main()

def Query(queryChoice):
    if queryChoice == "1":
        return random.choice(open('languages/english.txt').read().splitlines())
    elif queryChoice == "2":
        return random.choice(open('languages/turkish.txt').read().splitlines())
    elif queryChoice == "3":
        return random.choice(open('languages/german.txt').read().splitlines())
    elif queryChoice == "4":
        return random.choice(open('languages/japanese.txt').read().splitlines())
    elif queryChoice == "5":
        _files = os.listdir('languages/')
        number = random.randint(0, len(_files) - 1)
        file_ = _files[number]
        query = random.choice(open('languages/{}'.format(file_)).read().splitlines())
        return query
    

def ytfetch(queryChoice,videoAmount,videoDuration,keyword,orderBy):
    apiKey = open('apikey.txt').read()
    iteration = 1
    dumpvideos = {}
    videolist = []

    print("Do you want to give a name to the json file?")
    
    jsonQ = input("Y or N: ").lower()
                       
    if jsonQ.startswith("y"):
        jsonname = input("Enter a file name: ")
    else:
        jsonname = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
      
    while iteration <= videoAmount:
            #parsing url
            if queryChoice in ["1","2","3","4","5"]:
                query_ = Query(queryChoice)
                maxresults = 1
            else:
                query_ = keyword
                maxresults = videoAmount   
                
            query2_ = urllib.parse.quote_plus(query_)    

            urlData = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&videoDuration={}&order={}&q={}".format(apiKey,maxresults,videoDuration,orderBy,query2_)
            webURL = urllib.request.urlopen(urlData)
            data = webURL.read()
            encoding = webURL.info().get_content_charset('utf-8')
            results = json.loads(data.decode(encoding))
            
            if 'items' in results:
                if results['items'] == "":
                    iteration = iteration
                else:
                    for data in results['items']:
                        videoId = data['id']['videoId']
                        videoName = data['snippet']['title']
                        channelId = data['snippet']['channelId']
                        channelName = data['snippet']['channelTitle']
                        description = data['snippet']['description']
                        iteration = int(iteration)
                        # Another API request to get the duration:
                        contentDetails = json.loads(urllib.request.urlopen("https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={}&key={}".format(videoId,apiKey)).read())
                        duration = contentDetails['items'][0]['contentDetails']['duration']        
                        update = {str(iteration): {'query': query_, 'videoId': videoId, 'videoName': videoName, 'channelId': channelId, 'channelName': channelName, 'description': description, 'duration': duration}}
                        print("{}. {} - {}".format(iteration, query_, videoName))
                        dumpvideos.update(update)            
                        videolist.append(videoId)
                        iteration += 1
    

    with open('./json/{}.json'.format(jsonname), 'a') as outfile: 
        dumpdump = {"Search": {"searchDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "queryChoice:": keyword, "videoAmount": videoAmount, "videoDuration": videoDuration, "Order by": orderBy}}
        dumpdump.update({"Videos": dumpvideos})
        json.dump(dumpdump, outfile, indent=4, ensure_ascii = False)

    print("Finally, json file is ready!")
    print("So, would you like to download the videos? Y/N")
    dlChoice = input("Select: ").lower()

    if dlChoice.startswith("y"):
        ytDownload(jsonname,videolist)
    else:
        print("See ya!")


    
def ytDownload(jsonname, videolist):    
    
    os.mkdir("output/{}".format(jsonname))

    class MyLogger(object):
        def debug(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            print(msg)


    def my_hook(d):
        
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')


    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
 
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        os.chdir("output/{}".format(jsonname))
        ydl.download(videolist)



# Program Starts Here

print('Welcome my ladies and gentlemen to this wonderful youtube grabber/download software!')
print('============== version 1.something =================')

Main()





