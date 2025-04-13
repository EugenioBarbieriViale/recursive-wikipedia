import requests
import time
from random import randint
from bs4 import BeautifulSoup, SoupStrainer

url = "https://it.wikipedia.org"
rand_url = "http://en.wikipedia.org/wiki/Special:Random"

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def condition(s):
    return not ("Lingua" in s or "Lingue" in s or "Linguistica" in s or "Gnome" in s or "Aiuto" in s or "Categoria" in s)

def attempt(limit, query="", i=0):
    if i == 0:
        r = requests.get(rand_url, headers=headers)
    else:
        r = requests.get(url + query, headers=headers)

    soup = BeautifulSoup(r.content, "html.parser", parse_only=SoupStrainer('p'))

    for link in soup.find_all("a"):
        print(link)
        new_query = link.get("href")
        if new_query[0:6] == "/wiki/" and condition(new_query):
            break

    print(i, new_query)
    i += 1
    print("--------")

    if i < limit and new_query != "/wiki/Philosophy":
        time.sleep(1)
        return attempt(limit, new_query, i)

    elif i >= limit:
        print("NOT FOUND")
        return 0

    else:
        print("FOUND AFTER", i, "ATTEMPTS")
        return 1

attempt(5)
