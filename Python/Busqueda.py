import os
import re
import json
import requests
from bs4 import BeautifulSoup

def search(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for g in soup.find_all('g-card', class_='yXK7Te'):
        anchors = g.find_all('a')

        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').text
            snippet = g.find('span', class_='aCOpRe').text
            results.append({'title': title, 'link': link, 'snippet': snippet})

    return results

def main():
    query = input("Enter your search query: ")
    results = search(query)

    for i, result in enumerate(results, start=1):
        print(f"{i}. {result['title']}\n{result['link']}\n{result['snippet']}\n")

if __name__ == "__main__":
    main()