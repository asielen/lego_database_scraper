__author__ = 'andrew.sielen'

import requests
from bs4 import BeautifulSoup

url = "http://www.peeron.com/inv/sets/4431-1"
page = requests.get(url).content
soup = BeautifulSoup(page)

parent_tags = soup.find("div", {"class": "altsources"})
children_tags = parent_tags.findAll("li")

dic = {}
for i in children_tags:
    dic[i.contents[0].string.strip()] = i.contents[-1].string.strip()
    #i.contents[0] is the title tag / i.contents[-1] is the innermost tag

print(dic)