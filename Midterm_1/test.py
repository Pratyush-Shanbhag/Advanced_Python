import requests
from bs4 import BeautifulSoup

page = requests.get("https://gml.noaa.gov/aggi/aggi.html")
soup = BeautifulSoup(page.text, "html.parser")
elems = soup.select("td")
elems = [x.text for x in elems]
index = elems.index("1979")
for i in range(index, len(elems), 11):
    print(elems[i:i+11])

