import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def main(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # Find relevant data - inspect the page and adjust selectors accordingly
    # Example: Snow heights and snowfall might be in a specific div or span
    snow_data = soup.find_all("div", class_="table-data")  # Example selector
    list_group = snow_data[0].find("ul", class_="list-group")

    d = {"url": url, "date": datetime.today().strftime("%Y-%m-%d")}
    for row in list_group:
        s = row.text.strip()
        if s:
            k, v = s.split(":", 1)
            d[k] = v.strip()
    return d


if __name__ == "__main__":
    data = {}
    for url in open("urls.txt"):
        url = url.rstrip()
        d = main(url)
        _, name = url.rsplit("/", 1)
        data[name] = d
        print(name)
        print(d)
    json.dump(data, open("schneehoehen.json", "w"), indent=2)
