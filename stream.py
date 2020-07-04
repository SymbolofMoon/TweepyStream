import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import wget 
import requests
import cv2 
import sys
import getopt
import api_keys
import os
import pandas as pd
import numpy as np




auth = tweepy.OAuthHandler(api_keys.CONSUMER_KEY, api_keys.CONSUMER_SECRET)
auth.set_access_token(api_keys.ACCESS_TOKEN, api_keys.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

class TweetListener(StreamListener):
     #A listener handles tweets are the received from the stream.
    #This is a basic listener that just prints received tweets to standard output

    def on_data(self, data):
        print (data)
        return True

    def on_error(self, status):
        print (status)
#search
def info(username):
       api = tweepy.API(auth)
       twitterStream = Stream(auth,TweetListener())
       user = api.get_user(username)
       path="/home/prateek/PROGRAMS/mytwitterproject/{}".format(username)
       os.mkdir(path)
       
       file1 = open('/home/prateek/PROGRAMS/mytwitterproject/{}/{}.txt'.format(username,username),"w")
       file1.write(u"Name:{} \n".format(user.name).encode('utf-8'))

       file1.write(u"Location:{} \n".format(user.location).encode('utf-8'))
       file1.write(u"Description:{} \n".format(user.description).encode('utf-8'))
       file1.write(u"Created on: {} \n".format(user.created_at).encode('utf-8'))
       file1.write(u"Url Associated: {} \n".format(user.url).encode('utf-8'))
       file1.write(u"Profile Image: {} \n".format(user.profile_image_url).encode('utf-8'))
       file1.write(u"Total Followers: {} \n".format(user.followers_count).encode('utf-8'))
       file1.write(u"Status count: {} \n".format(user.statuses_count).encode('utf-8'))
       file1.write(u"Total following:{} \n".format(user.friends_count).encode('utf-8'))

       file1.close()
       print(u"Name:{} \n".format(user.name).encode('utf-8'))
       print(u"Location:{} ".format(user.location).encode('utf-8'))
       print(u"Description:{} ".format(user.description).encode('utf-8'))
       print(u"Created on: {} ".format(user.created_at).encode('utf-8'))
       print(u"Url Associated: {} ".format(user.url).encode('utf-8'))
       print(u"Profile Image: {} ".format(user.profile_image_url).encode('utf-8'))
       print(u"Total Followers: {} ".format(user.followers_count).encode('utf-8'))
       print(u"Status count: {} ".format(user.statuses_count).encode('utf-8'))
       print(u"Total following:{} ".format(user.friends_count).encode('utf-8'))

       
       
       target_path='/home/prateek/PROGRAMS/mytwitterproject/{}/{}.jpg'.format(username,username)
       profile_pic=wget.download(user.profile_image_url,target_path)
       
       
       
       
       print("Created {}.txt and profile pic of {}".format(username, username))   

            
        
def twiiter_media(username):
        api = tweepy.API(auth)
        tweets = api.user_timeline(screen_name=username,
                           count=200, include_rts=False,
                           exclude_replies=False)
        id=[]
        date=[]
        tweet_text=[]
        image_url=[]
        #id=list()
        count = 1
        for status in tweets:  
                media = status.entities.get('media', [])
                user_mention = status.entities.get('user_mentions', [])
                if(len(media) > 0):
                       print("--------------------------------------------------###################################################------------------------------------")
                       print("{}.".format(count))
                       count=count+1
                       id.append(status.id)
                       date.append(status.created_at)
                       tweet_text.append(status.text.encode("utf-8"))
                       image_url.append(media[0]['media_url'])
                       print("Id : {}".format(status.id))
                       print("Date And Time: {}".format(status.created_at))
                       print(u"Tweet is : {} ".format(status.text).encode("utf-8"))
                       print("Image Url : {}".format(media[0]['media_url']))
                       img_url = media[0]['media_url']
                       target_path='/home/prateek/PROGRAMS/mytwitterproject/{}/{}.jpg'.format(username,status.id)
                       profile_pic=wget.download(img_url,target_path)
                       for i in  range(len(user_mention)):
                          print("Mention Username are : {}".format(user_mention[i]['screen_name']))      
                       print("\n")               


def tweets_to_data_frame(username):
        api = tweepy.API(auth)
        tweets = api.user_timeline(screen_name=username,
                           count=20 )
        df = pd.DataFrame(data=[tweet.id for tweet in tweets], columns=['id'])
        
        df['date'] = np.array([tweet.created_at for tweet in tweets])
       # 
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['Retweet Count'] = np.array([tweet.retweet_count for tweet in tweets])
        df['Tweets'] = np.array([tweet.text.encode("utf-8").decode("utf-8") for tweet in tweets])
        return df
if __name__ == '__main__':
    def main(argv):
        main.username=''
        try:
           opts, args = getopt.getopt(argv,"hu:o:",["uername=","outputfile="])
        except getopt.GetoptError:
            print ('stream.py -u <username> ')
            sys.exit(2)
        for opt, arg in opts:
           if (opt == '-h'):
                print ('stream.py -u <username> ')
                sys.exit()
           elif opt in ("-u", "--username"):
               main.username = arg    
               info(main.username)
               print("#------------------------ Media Files-----------------------------# ")
               
               twiiter_media(main.username)
               print("#----------------------- Tweet Records--------------------------#")
               
               
               df = tweets_to_data_frame(main.username)
               print(df)
               path_for_csv='/home/prateek/PROGRAMS/mytwitterproject/{}/{}.csv'.format(main.username,main.username)
               df.to_csv(path_for_csv, index=False,encoding='utf-8')
           else:
               print("Usage python stream.py -u <username>")
                

    main(sys.argv[1:])
    
          




    