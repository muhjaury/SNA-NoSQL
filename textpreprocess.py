#!/usr/bin/python
""" 
    Muhammad Nur Yasir Utomo
    yasirutomo@gmail.com
"""

import re
from nltk.tokenize import RegexpTokenizer

#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL) 
    return pattern.sub(r"\1\1", s)
#end

# Text normalization
def preprocessdata(text):
    text = text.replace("\n", "")
    text = "".join([x for x in text if ord(x)<128])
    text = text.replace("'", "")
    text = text.replace('"', '')
    text = re.sub('[\s]+', ' ', text)
    text = text.strip()

    return text

def textpreprocessSenti(text):
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',text)
    text = re.sub(r'\(',' ( ',text)
    text = re.sub(r'\)',' ) ',text)
    text = re.sub(r'\[',' [ ',text)
    text = re.sub(r'\]',' ] ',text)
    text = text.replace("@", "")
    text = text.replace("#", "")
    text = text.replace("_", " ")
    text = text.replace("&amp;","and")
    text = text.replace("&lt;","")
    text = text.replace("&gt;","")
    text = re.sub('\,+',',',text)
    text = re.sub('\.+','.',text)
    text = re.sub('\/+','/',text)
    text = re.sub('\|+','|',text)
    text = re.sub('\?+','?',text)
    text = re.sub('\!+','!',text)
    text = re.sub('\:+',':',text)
    text = re.sub('\%+','%',text)
    text = re.sub('\=+','=',text)
    text = re.sub('\-+','-',text)
    text = text.replace(",", " , ")
    text = text.replace(".", " . ")
    text = text.replace("/", " / ")
    text = text.replace("|", " | ")
    text = text.replace("?", " ? ")
    text = text.replace("!", " ! ")
    text = text.replace(":", " : ")
    text = text.replace("%", " % ")
    text = text.replace("=", " = ")
    text = text.replace("-", " - ")
    text = text.replace(";", " ; ")
    text = re.sub('[\s]+', ' ', text)
    text = text.strip()
    text = text.lower()

    return text

def textpreWordFeature(text):
    #Convert to lower case
    text = text.lower()
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',text)
    text = re.sub(r'\(',' ( ',text)
    text = re.sub(r'\)',' ) ',text)
    text = re.sub(r'\[',' [ ',text)
    text = re.sub(r'\]',' ] ',text)
    text = text.replace("_", " ")
    text = text.replace("&amp;","and")
    text = text.replace("&lt;","")
    text = text.replace("&gt;","")
    text = re.sub('\,+',',',text)
    text = re.sub('\.+','.',text)
    text = re.sub('\/+','/',text)
    text = re.sub('\|+','|',text)
    text = re.sub('\?+','?',text)
    text = re.sub('\!+','!',text)
    text = re.sub('\:+',':',text)
    text = re.sub('\%+','%',text)
    text = re.sub('\=+','=',text)
    text = re.sub('\-+','-',text)
    text = text.replace(",", " , ")
    text = text.replace(".", " . ")
    text = text.replace("/", " / ")
    text = text.replace("|", " | ")
    text = text.replace("?", " ? ")
    text = text.replace("!", " ! ")
    text = text.replace(":", " : ")
    text = text.replace("%", " % ")
    text = text.replace("=", " = ")
    text = text.replace("-", " - ")
    text = text.replace(";", " ; ")
    text = re.sub('@[^\s]+','AT_USER',text)    
    text = re.sub(r'#([^\s]+)', r'\1', text)
    text = re.sub('[\s]+', ' ', text)
    text = text.strip()

    return text