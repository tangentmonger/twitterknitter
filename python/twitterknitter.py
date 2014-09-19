""" Runs the TwitterKnitter. Prepares images and
sends them to the Arduino one line at a time. """

from knitter24 import Knitter24
from pattern24 import Pattern24
from TwitterSearch import *
from secrets import Secrets
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


def choose_tweet():
    """Offers a text-based menu of tweet text to knit"""
    tweets = get_tweets()
    chosen = False
    while(not(chosen)):
        print("0: <REFRESH TWEETS>")
        for idx, tweet in enumerate(tweets):
            print ("%d: %s" % (idx+1, tweet))
        print("%d: <ENTER TEXT>" % (len(tweets) + 1))
        print
        selection = input('Choose a tweet: ')
        try:
            number = int(selection)
            if(number == 0):
                tweets = get_tweets()
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
    """Fetches up to 10 tweets and returns their text in a list"""
    hashtag = "maker"

    sources = []
    try:
        tso = TwitterSearchOrder()
        tso.setSearchURL("?q=%23" + hashtag)
        tso.setLocale('en')
        tso.setCount(10)
        tso.setIncludeEntities(False)

        twitter_search = TwitterSearch(
            consumer_key = Secrets.consumer_key,
            consumer_secret = Secrets.consumer_secret,
            access_token = Secrets.access_token,
            access_token_secret = Secrets.access_token_secret
            )

        tweets = twitter_search.searchTweets(tso)

        for tweet in tweets['content']['statuses']:
            sources.append(tweet['text'])

    except TwitterSearchException as exception:
        print(exception)

    return sources


def create_image_from_text(text):
    """Creates a 24-pixel wide image featuring the given text"""
    try:
        text = text.encode('ascii', 'ignore')
        #no TTF, they get antialiased!
        font = ImageFont.load("fonts/helvB12.pil") #22, clear
        #font = ImageFont.load("courB14.pil") #20 pixels, bold ish
        #font = ImageFont.load("charR14.pil") #23, seify
        #font = ImageFont.load("timR14.pil") #22, ick
        #font = ImageFont.load("term14.pil") #22, ick

        width, height = font.getsize(text)
        border_width = 2

        img = Image.new("1", (border_width*2 + width, 24), 1)
        #24 pixels high, length is arbitrary
        width, height = img.size
        draw = ImageDraw.Draw(img)
        draw.line(((0, 1), (width, 1)), fill=0)
        draw.line(((0, height - 2), (width, height - 2)), fill=0)
        draw.text((border_width, border_width), text, 0, font=font)
        draw = ImageDraw.Draw(img)
        img = img.rotate(90)
        img.save("a_test.png")
        return img
    except Exception as exception:
        print(exception)

#text = choose_tweet()
text = input("Enter text: ")
#pattern = Pattern24.from_test_columns()
#pattern = Pattern24.from_test_rows()
#image = Image.open("/home/coryy/Dropbox/knitsnake/snakepattern2.bmp")
image = create_image_from_text(text)
pattern = Pattern24.from_image(image)

knitter = Knitter24("/dev/ttyUSB0", 9600)
knitter.send_pattern(pattern)

