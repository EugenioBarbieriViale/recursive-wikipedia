import requests
import time
from bs4 import BeautifulSoup, SoupStrainer

url = "https://it.wikipedia.org"

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def condition(s):
    return not ("Lingua" in s or "Lingue" in s or "Linguistica" in s or "Gnome" in s or "Aiuto" in s)

def get(query, limit, i=0):
    r = requests.get(url + query, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser", parse_only=SoupStrainer('p'))

    for link in soup.find_all("a"):
        new_query = link.get("href")
        if new_query[0:6] == "/wiki/" and condition(new_query):
            break

    print(i, new_query)
    i += 1

    if i < limit and new_query != "/wiki/Filosofia":
        time.sleep(1)
        return get(new_query, limit, i)

    elif i >= limit:
        print("NOT FOUND")
        return ""

    else:
        print("FOUND AFTER", i, "ATTEMPTS")
        return ""

query = "/wiki/Abbigliamento"
get(query, 15)
