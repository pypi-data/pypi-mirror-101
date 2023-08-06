"""
Author : Jung Hoon, Lee
Editor : Jin Uk, Cho
Last update : 12th, Apr, 2020
"""
import requests
from bs4 import BeautifulSoup
import random

from ..file_utils import open_text
import os
# path = os.path.join(os.path.curdir, "../stopwords-ko.txt")
path = os.path.abspath("ktextaug/stopwords-ko.txt")
# print("exist?", os.path.exists(path)) # /home/jucho/PythonProjects/textaug/kTextAugmentation/ktextaug/stopwords-ko.txt
# print("same?", "/home/jucho/PythonProjects/textaug/kTextAugmentation/ktextaug/stopwords-ko.txt" == path)
# print(path)
stopwords = open_text(path)


def isWord(word):
    return word.isalnum()

def isStopword(word):
    if word in stopwords:
        return True
    else:
        return False

def get_synonym(word):
    relate_list = []
    res = requests.get("https://dic.daum.net/search.do?q=" + word)
    soup = BeautifulSoup(res.content, "html.parser")
    try:
        word_id = soup.find("ul", class_="list_relate")
    except AttributeError:
        return word
    if word_id == None:
        return word
    for tag in word_id.find_all("a"):
        relate_list.append(tag.text)

    return random.choice(relate_list)

if __name__ == "__main__":
    print(isStopword("아홉"))
