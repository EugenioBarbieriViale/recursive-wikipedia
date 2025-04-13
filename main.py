import requests
import time
from random import randint
from bs4 import BeautifulSoup, SoupStrainer
from csv import writer

# number of requests
n = 2

# number of links to open per page
x = 15


url = "https://en.wikipedia.org"
rand_url = "http://en.wikipedia.org/wiki/Special:Random"

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def condition(s):
    return not ("Help" in s or "Special" in s)

arr = []

def attempt(limit, query="", i=0):
    s = requests.Session()
    s.cookies["news.lang"] = "en"

    if i == 0:
        r = s.get(rand_url, headers=headers)
    else:
        r = s.get(url + query, headers=headers)

    soup = BeautifulSoup(r.content, "html.parser", parse_only=SoupStrainer('p'))

    for link in soup.find_all("a"):
        new_query = link.get("href")
        if new_query[0:6] == "/wiki/" and condition(new_query):
            break

    print(i, new_query)
    i += 1

    arr.append(new_query[6:])

    if new_query == "/wiki/Philosophy" or new_query == "/wiki/Philosophical" or i >= limit:
        return arr

    if i < limit and (new_query != "/wiki/Philosophy" or new_query != "/wiki/Philosophical"):
        time.sleep(1)
        return attempt(limit, new_query, i)

head = [str(i) for i in range(x)]
data = [head]

for i in range(n):
    attempt(x)
    print(arr)

    if len(arr) < x:
        for j in range(x-len(arr)):
            arr.append("")

    data.append(arr)
    arr = []

with open("collection.csv", mode="w", newline="") as f:
    w = writer(f)
    w.writerows(data)
