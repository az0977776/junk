import requests
from bs4 import BeautifulSoup

# looks like the zip refers to free items
base_url = "https://newyork.craigslist.org/search/zip"

def get_items_html(offset, query=""):
    if query != "":
        url = f"{base_url}?s={offset}&query={query}"
    else:
        url = f"{base_url}?s={offset}"

    r = requests.get(url)
    assert r.status_code == 200
    return r.text.encode("utf-8")

# returns dict of {name:link}
def parse_items(html):
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.findAll("li", {"class": "result-row"})

    item_links = {}
    for item in items:
        k = item.findAll("a")[1]
        if k.contents[0] in item_links.keys():
            print(f"found a dupe: {k.contents[0]}\n")
        item_links[k.contents[0].encode("utf-8")] = k["href"].encode("utf-8")

    return item_links


def search(query="", limit=500):
    items = {}
    offset = 0

    while True:
        html = get_items_html(offset, query)
        items_d = parse_items(html)
        items.update(items_d)
        if len(items_d) < 120:
            break
        if len(items) > limit:
            break
        # this should be 120 each time if full page
        offset += len(items_d)

    return items


if __name__ == "__main__":
    res = search("shoes")
    print(res.keys())