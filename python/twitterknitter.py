""" Runs the TwitterKnitter. Prepares images and
sends them to the Arduino one line at a time. """

from knitter24 import Knitter24
from pattern24 import Pattern24
from TwitterSearch import *
from secrets import Secrets
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import requests
import re


def choose_tweet():
    """Offers a text-based menu of tweet text to knit"""
    tweets = get_tweets_genes()
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
                tweets = get_tweets_genes()
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

def get_tweets_genes():
    """Fetches up to 10 tweets and returns their text in a list"""
    hashtag = "makerprintgenes"

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

def find_gene_id(tweet):

    tweet = re.sub("(?i)#makerprintgenes", "", tweet)

    # Expected tweet format "Gene-symbol Species #MakerPrintGenes"
    # Eg. "BRCA1 human #MakerPrintGenes"
    # "BRAFP1 homo sapien #MakerPrintGenes"
    # "BRCA2 mouse #MakerPrintGenes"
    # "MT-TV human #MakerPrintGenes"
    queries = tweet.strip().split(" ", 1)

    gene_symbol = queries[0]
    species = queries[1]

    # Lookup searches for a specific gene using the gene-symbol and species
    base_url = "http://rest.ensembl.org/lookup/symbol/"
    request_params = "?content-type=application/json"

    try:
        r = requests.get(base_url+species+"/"+gene_symbol+request_params,
                         headers={"Content-Type": "application/json"})
        r.raise_for_status()

        response = r.json()

        # Now that Gene-ID found use this to get gene (& protein) sequence(s)
        return get_gene_sequences(response["id"], response["biotype"])
    except requests.exceptions.HTTPError as errh:
        print ("http error for gene id request:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting for gene id request:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error for gene id request:",errt)
    except requests.exceptions.RequestException as err:
        print('Request to find gene ID from Ensembl failed.')
        print (err)
    return

def get_gene_sequences(gene_id, gene_type):

    # Sequence API endpoint requires an Ensembl ID
    base_url = "http://rest.ensembl.org/sequence/id/"
    request_params = "?content-type=application/json&type="

    transcript_id = ""
    nucleotide_seq = ""

    # If the gene is protein-coding we want both the coding sequence (CDS) and
    # the translated protein sequence
    if gene_type == 'protein_coding':
        # Specify multiple_sequences=1 as there can be multiple transcripts for
        # each gene. A typical strategy is to choose the longest transcript that
        # includes most(/all) of the gene's coding sequence
        r = requests.get(base_url+gene_id+request_params+"cds&multiple_sequences=1",
                         headers={"Content-Type": "application/json"})

        sequences = r.json()

        # If there's more than one sequence we want to choose the longest,
        # reverse sorting puts that sequence first
        if len(sequences) > 1:
            sequences = sorted(sequences, key = lambda i: len(i["seq"]), reverse=True)

        # Now that we have the longest (or only) sequence first, we want to take
        # note of that specific transcript ID so that we can request the
        # matching translated protein sequence for that transcript.
        # This avoids a case arising where two transcripts have the same
        # length and the wrong protein sequence is chosen to match the
        # nucleotide sequence.
        transcript_id = sequences[0]["id"]
        nucleotide_seq = sequences[0]["seq"]

        r = requests.get(base_url+transcript_id+request_params+"protein",
                         headers={"Content-Type": "application/json"})
        protein = r.json()

        # Spacing added to amino acid sequence so that it aligns to nucleotide
        # coding sequence later
        protein_seq = " " + "  ".join(protein["seq"]) + " "

        # Return both the coding sequence and the protein sequence so they can
        # be printed together
        return [nucleotide_seq, protein_seq]

    else:

        # If this isn't a protein-coding gene then just fetch the cDNA sequence
        r = requests.get(base_url+gene_id+request_params+"cdna&multiple_sequences=1",
                         headers={"Content-Type": "application/json"})
        sequences = r.json()

        if len(sequences) > 1:
            sequences = sorted(sequences, key = lambda i: len(i["seq"]), reverse=True)

        nucleotide_seq = sequences[0]["seq"]

        # Return just the nucleotide sequence
        return nucleotide_seq

def create_image_from_text(text):

    """Creates a 24-pixel wide image featuring the given text"""
    try:
        #text = text.encode('ascii', 'ignore')
        #no TTF, they get antialiased!
        #font = ImageFont.load("fonts/helvB12.pil", 22) #22, clear
        #font = ImageFont.truetype("fonts/FreeMonoBold.ttf", 14) #22, clear
        #font = ImageFont.truetype("fonts/RobotoMono-Regular.ttf", 11) #22, clear
        font = ImageFont.truetype("fonts/RobotoMono-Bold.ttf", 11) #22, clear
        #font = ImageFont.load("courB14.pil") #20 pixels, bold ish
        #font = ImageFont.load("charR14.pil") #23, seify
        #font = ImageFont.load("timR14.pil") #22, ick
        #font = ImageFont.load("term14.pil") #22, ick

        border_width = 1

        # Determine if `text` is a string - if it is then it just contains the
        # nucleotide sequence for a gene that is not protein-protein_coding
        # If `text` is not a string then it's protein-coding and should be a
        # list with a corresponding protein sequence

        if isinstance(text, str):

            # NON-CODING GENES
            # ----------------

            width, height = font.getsize(text)

            # bonds = text.replace("C", "…").replace("G", "…").replace("A", "‥").replace("T", "‥")

            # Generate a complementary DNA sequence to base pair with for printing
            #complement_mapping = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
            #complement = "".join(complement_mapping.get(base, base) for base in text)

            #Trying make trans
            transTable = str.maketrans("ATGC", "TACG")
            complement =  str.translate(text, transTable)

            img = Image.new("1", (border_width*2 + width, 24), 1)
            #24 pixels high, length is arbitrary
            width, height = img.size

            print("width", width, "height", height)
            draw = ImageDraw.Draw(img)
            draw.fontmode = "1"
            draw.line(((0, 1), (width, 1)), fill=0)
            draw.line(((0, height - 2), (width, height - 2)), fill=0)

            # Draw gene sequence
            draw.text((border_width, 1), text, 0, font=font)
            #draw.text((border_width, border_width+1), bonds, 0, font=font)

            # Draw complementary DNA sequence
            draw.text((border_width, border_width+9), complement, 0, font=font)
            draw = ImageDraw.Draw(img)
            img = img.rotate(-90, expand=1)

            #width, height = img.size
            #print("width", width, "height", height)
            img.save("b_test.png")
            return img
        else:

            # PROTEIN-CODING GENES
            # --------------------

            # Get size of nucleotide sequence
            width, height = font.getsize(text[0])

            img = Image.new("1", (border_width*2 + width, 24), 1)
            #24 pixels high, length is arbitrary
            width, height = img.size

            print("width", width, "height", height)
            draw = ImageDraw.Draw(img)
            draw.fontmode = "1"
            draw.line(((0, 1), (width, 1)), fill=0)
            draw.line(((0, height - 2), (width, height - 2)), fill=0)

            # Draw DNA coding sequence
            draw.text((border_width, 0), text[0], 0, font=font)

            # Draw protein sequence
            draw.text((border_width, border_width+7), text[1], 0, font=font)
            draw = ImageDraw.Draw(img)
            img = img.rotate(-90, expand=1)

            #width, height = img.size
            #print("width", width, "height", height)
            img.save("b_test.png")
            return img
    except Exception as exception:
        print(exception)

tweet = choose_tweet()
text = find_gene_id(tweet)
#text = input("Enter text: ")
#pattern = Pattern24.from_test_columns()
#pattern = Pattern24.from_test_rows()
#image = Image.open("../img/at_test1.bmp")
image = create_image_from_text(text)
pattern = Pattern24.from_image(image)

knitter = Knitter24("/dev/ttyUSB2", 9600)
knitter.send_pattern(pattern)
