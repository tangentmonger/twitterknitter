from knitter24 import Knitter24
from pattern24 import Pattern24
from TwitterSearch import *
from secrets import Secrets
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


def choose_tweet():
    tweets = get_tweets()
    chosen = False
    while(not(chosen)):
        print("0: <REFRESH TWEETS>")
        for idx, tweet in enumerate(tweets):
            print ("%d: %s" % (idx+1, tweet))
        print("%d: <ENTER TEXT>" % (len(tweets) + 1))
        print
        nb = input('Choose a tweet: ')
        try:
            number = int( nb )
            if(number == 0):
                tweets = getTweets()
            elif(0 < number <= len(tweets)):
                text = tweets[number-1]
                chosen = True
            elif(number == len(tweets)+1):
                text = input("Enter text: ")
                chosen = True
            else:
                print("Not a tweet! Try again")
        except:
            print( "Invalid number" )
    return text

def get_tweets():

    hashtag = "maker"

    sources = []
    try:
        tso = TwitterSearchOrder()
        tso.setSearchURL("?q=%23" + hashtag)
        tso.setLocale('en')
        tso.setCount(10)
        tso.setIncludeEntities(False)

        ts = TwitterSearch(
            consumer_key = Secrets.consumer_key,
            consumer_secret = Secrets.consumer_secret,
            access_token = Secrets.access_token,
            access_token_secret = Secrets.access_token_secret
            )

        tweets = ts.searchTweets(tso)

        for tweet in tweets['content']['statuses']:
            sources.append(tweet['text'])

    except TwitterSearchException as e:
        print(e)

    return sources


def create_image_from_text(text):
    try:
        text = text.encode('ascii', 'ignore')
        #no TTF, they get antialiased!
        font = ImageFont.load("fonts/helvB12.pil") #22, clear
        #font = ImageFont.load("courB14.pil") #20 pixels, bold ish
        #font = ImageFont.load("charR14.pil") #23, seify
        #font = ImageFont.load("timR14.pil") #22, ick
        #font = ImageFont.load("term14.pil") #22, ick

        width, height = font.getsize(text)
        borderWidth = 2;

        img=Image.new("1", (borderWidth*2 + width, 24),1) #24 pixels high, length is arbitrary
        width, height = img.size
        draw = ImageDraw.Draw(img)
        draw.line(((0, 1), (width, 1)), fill=0)
        draw.line(((0, height - 2), (width, height - 2)), fill=0)
        draw.text((borderWidth, borderWidth),text,0,font=font)
        draw = ImageDraw.Draw(img)
        img = img.rotate(90)
        img.save("a_test.png")
        return img
    except Exception as e:
        print(e)

while(True):

    pattern = Pattern24.from_test_columns()
    
    knitter = Knitter24()
    knitter.send_pattern(pattern)

    input("Press any key to continue")
