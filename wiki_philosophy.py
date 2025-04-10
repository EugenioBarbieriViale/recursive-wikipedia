import requests
import time
from bs4 import BeautifulSoup, SoupStrainer

url = "https://it.wikipedia.org"

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def condition(s):
    return not ("Lingua" in s or "Lingue" in s or "Linguistica" in s or "Gnome" in s or "Aiuto" in s or "Categoria" in s)

def random_noun():
    url = "https://www.parolecasuali.it/?fs=1&fs2=0&Submit=Nuova+parola"
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.content, "html.parser")
    word = soup.find("div", attrs={"style" : "font-size:3em; color:#6200C5;"}).text
    return word

def word_to_query():
    query = f"/wiki/{random_noun()}".replace("\n", "")
    r = requests.get(url + query, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser", parse_only=SoupStrainer('p')).text

    print(query, soup)
    if soup == "":
        word_to_query()
    else:
        return query

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
        time.sleep(2)
        return get(new_query, limit, i)

    elif i >= limit:
        print("NOT FOUND")
        return 0

    else:
        print("FOUND AFTER", i, "ATTEMPTS")
        return 1

n = 10
n_recursions = 5
count = 0

for i in range(n):
    query = f"/wiki/{random_noun()}".replace("\n", "")
    print(query)
    # attempt = get(word_to_query(), n_recursions)
    attempt = get(query, n_recursions)

    if attempt == 1:
        count += 1

print(count / n * 100, "%")
