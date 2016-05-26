#!/usr/bin/env python
__author__ = "Victor Cortez"
__version__ = "1.0"
__maintainer__ = "Victor Cortez"
__email__ = "victorcortezcb@gmail.com"
__status__ = "In Production"
# We are going to use only this module
import requests
# Simple function to help checking if the inputs are correct
def check(string,target):
    # Filtering the incompatible characters
    newstring = "".join([i for i in string if i in target])
    # Comparing the two string to check if there was any modification
    if newstring == string:
        return True
    else:
        return False
    # If where was not, return true, if there was, return false
# Main function to retrieve you the book desired
def getbook(hexagon,wall,shelf,volume):
    # The title is expandable, in the inputs of the fuction you can see very easily what you need
    # Just formatting the volume variable to fulfill the protocol the site wants
    if int(volume) <= 9:
        volume = "0" + volume
    # Alphabet and numbers allow in the website, just for checking
    alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    numbers = ["0","1","2","3","4","5","6","7","8","9"]
    # Basic checking to make sure your inputs are correct
    if check(hexagon,alphabet + numbers) is False:
        raise Exception('Hexagon data format incorrect')
    if check(wall,numbers) is False or int(wall) > 4 or int(wall) < 1:
        raise Exception('wall data format incorrect or in incorrect range(1-4)')
    if check(shelf,numbers) is False or int(shelf) > 5 or int(shelf) < 1:
        raise Exception('shelf data format incorrect or in incorrect range (1-5)')
    if check(volume,numbers) is False or int(volume) > 32 or int(volume) < 1:
        raise Exception('volume data format incorrect or in incorrect range (1-32)')
    # Making the request with the data provided
    form = {"hex":hexagon,"wall":wall,"shelf":shelf,"volume":volume,"page":"1","title":"startofthetext"}
    url = "https://libraryofbabel.info/download.cgi"
    text = requests.post(url,data=form)
    # Cleaning the raw text, so "content" turns into the pure book
    content = text.text[len("startofthetext")+ 2::].rsplit('\n', 4)[0]
    return content
