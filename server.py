import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import serial
import urllib
import json
import oauth






def getTweets():

    tweets = []
    search_results = oauth.search_for_a_tweet(bearer_token, '%23'+ourHashtag) # does a very basic search
    json_results = json.loads(search_results)

    if "statuses" in json_results:
        for result in json_results["statuses"]:
            text = result["text"]
            for hashtag in result["entities"]["hashtags"]:
                tag =  hashtag["text"]
            
                #text = text.replace("#"+hashtag["text"], "")
            text = text.encode('ascii', 'ignore')
            text = text.replace("\n", " ")
            tweets.append(text)

    return tweets



def chooseTweet(tweets):
    chosen = False
    while(not(chosen)):
        print("0: <REFRESH TWEETS>")
        for i in range(0,len(tweets)):
            print ("%d: %s" % (i+1, tweets[i]))
        print("%d: <ENTER TEXT>" % (len(tweets) + 1))
        print
        nb = input('Choose a tweet: ')
        try:
            number = int( nb )
            if(number == 0):
                tweets = getTweets()
            elif(number > 0 and number <= len(tweets)):
                text = tweets[number-1]
                chosen = True
            elif(number == len(tweets)+1):
                text = raw_input("Enter text: ")
                chosen = True
            else:
                print("Not a tweet! Try again")
        except:
            print( "Invalid number" )
    return text


def sendPattern(text):

    try:
        # easiest version: text in one row

        #no TTF, they get antialiased!
        #font = ImageFont.load("courB14.pil") #20 pixels, bold ish
        #font = ImageFont.load("charR14.pil") #23, seify
        font = ImageFont.load("helvB12.pil") #22, clear
        #font = ImageFont.load("timR14.pil") #22, ick
        #font = ImageFont.load("term14.pil") #22, ick



        #how long is this text?
        width, height = font.getsize(text)
        borderWidth = 2;
        print(height)


        img=Image.new("1", (borderWidth*2 + width, 24),1) #24 pixels high, length is arbitrary
        width, height = img.size
        draw = ImageDraw.Draw(img)
        draw.line(((0, 1), (width, 1)), fill=0)
        draw.line(((0, height - 2), (width, height - 2)), fill=0)
        draw.text((borderWidth, borderWidth),text,0,font=font)
        draw = ImageDraw.Draw(img)
        img = img.rotate(90)
        img.save("a_test.png")


        #then read out as if for knitting
        #may have to reverse this, not sure?
        rawPattern = list(img.getdata())
        #print rawPattern

        def binify(x): 
            if (x == 0):
                return '0' 
            else:
                return '1'

        binaryPattern = map(binify, rawPattern)

        binaryPatternString = ''.join(binaryPattern)
        #print binaryPatternString


        columns, rows = img.size;
        #assert: columns == 24

        ser = serial.Serial('/dev/ttyUSB0', 9600) #or whatever

        #ser.write(chr(1))
        #ser.write(chr(1))
        #ser.write(chr(0))
        #ser.write(chr(0))
       
        #exit


        #ser.write(chr(3))#--
        #ser.write(chr(0))
        #ser.write(chr(0))
        #ser.write(chr(0))#--
        #ser.write(chr(0))
        #ser.write(chr(0))
        #ser.write(chr(3))#--
        #ser.write(chr(0))
        #ser.write(chr(0))
        #exit

        ser.write(chr(rows)) #number of rows

        for i in range(0,rows):
            binaryRowData = binaryPatternString[0:24]
            print binaryRowData
            binaryPatternString = binaryPatternString[24:]

            for group in reversed(range(0,3)):
                byteString = binaryRowData[group*8:(group+1)*8]
                print byteString
                data = int(byteString,2)
                #print data
                ser.write(chr(data))
        print("Pattern sent!")
        print

    except:
        print("Failed to send pattern")
        print


#Toglodytes: secrets are on the wiki :)
ourHashtag = "DMMFknitter"
consumer_key = 'xxxx' # put your apps consumer key here 
consumer_secret = 'xxxx' # put your apps consumer secret here
bearer_token = oauth.get_bearer_token(consumer_key,consumer_secret) # generates a bearer token


while(True):
    tweets = getTweets()
    text = chooseTweet(tweets)
    sendPattern(text)


