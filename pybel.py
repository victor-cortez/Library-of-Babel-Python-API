#!/usr/bin/env python
__author__ = "Victor Barros"
__version__ = "1.1"
__maintainer__ = "Victor Barros"
__email__ = "victorcortezcb@gmail.com"
__status__ = "In Production"
# We are going to use only these two modules
import requests
from bs4 import BeautifulSoup, element
import re
import random as rnd
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
def browse(hexagon,wall,shelf,volume):
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

class SearchResult:
    def __init__(self, hexagon, wall, shelf, volume,page, position):
        self.type = type
        self.page = page
        self.hexagon = hexagon
        self.wall = wall
        self.shelf = shelf
        self.volume = volume
        self.page = page
        self.position = position
    
def process_search_result(result):
    try:
        type = result.find("h3").text
    except Exception as e:
        raise Exception("Result parsing error: " + str(e))
    title_and_page = [i.text for i in result.find_all("b")]
    if (len(title_and_page) == 2):
        title,page = title_and_page
    elif (len(title_and_page) == 1):
        title = title_and_page[0]
        page = None
    else:
        raise Exception("Unexpected title and page format")
    info = result.find("a",{"class":"intext"})["onclick"]
    data_points = re.findall(r"'(\w+)'", info)
    if (len(data_points) not in [5,7]):
        raise Exception("Unexpected book address format")
    hexagon,wall,shelf,volume,page = data_points[0:5]
    if len(data_points) == 7:
        position = data_points[5]
    else:
        position = None
    return SearchResult(hexagon, wall, shelf, volume,page,position)


def search(book_text):
    form = {"find":book_text}
    url = "https://libraryofbabel.info/search.cgi"
    text = requests.post(url,data=form)
    content_soup = BeautifulSoup(text.text)
    search_raw_results = content_soup.find_all("div", {"class": "location"})
    return [process_search_result(i) for i in search_raw_results if type(i) == element.Tag]

def random(hexagon_name_length=3200):
    hexagon = "".join([rnd.choice("abcdefghijklmnopqrstuvwxyz0123456789") for i in range(hexagon_name_length)])
    wall = str(rnd.randint(1,4))
    shelf = str(rnd.randint(1,5))
    volume = str(rnd.randint(1,32))
    return browse(hexagon,wall,shelf,volume)
