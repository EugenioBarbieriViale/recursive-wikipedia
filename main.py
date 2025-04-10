import requests
import time
from random import randint
from bs4 import BeautifulSoup, SoupStrainer

url = "https://it.wikipedia.org"

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def condition(s):
    return not ("Lingua" in s or "Lingue" in s or "Linguistica" in s or "Gnome" in s or "Aiuto" in s or "Categoria" in s)

def attempt(query, limit, i=0):
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
        return attempt(new_query, limit, i)

    elif i >= limit:
        print("NOT FOUND")
        return 0

    else:
        print("FOUND AFTER", i, "ATTEMPTS")
        return 1

def get_query(theme):
    s = requests.Session()

    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "list": "allpages",
        "apfrom": theme,
        # "aplimit": 100,
    }

    r = s.get(url=url, params=params)
    data = r.json()

    pages = data["query"]["allpages"]

    return pages[randint(0, len(pages))]["title"].replace("!", "")

theme = "scienza"
for i in range(10):
    query = "/wiki/" + get_query(theme)
    print(query)

    attempt(query, 15)
