
import requests
import random
from bs4 import BeautifulSoup 
import json 
import ssl
from nostr.event import Event
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType
from nostr.key import PrivateKey
from nostr.key import PublicKey
import yaml 

url = 'https://feeds.npr.org/sections/news/'

r = requests.get(url)

soup = BeautifulSoup(r.content, 'html.parser')
articles = soup.select('article h2 a')

news_list = []
for i in articles:
    article = str(i)
    article = article.split('href="', 1)[1].split("</a>", 1)[0]
    url = article.split('">',1)[0]
    tagline = article.split('">',1)[1]
    news_list.append([tagline,url])

url = 'https://www.reuters.com/news/archive/rates-rss'

r = requests.get(url)


soup = BeautifulSoup(r.content, 'html.parser')

articles = soup.select("article", class_="div")

reuters_prefix = "https://www.reuters.com"


for i in articles:
    article = i.find("div", class_="story-content")
    article = article.find("a", href=True)
    url = reuters_prefix + str(article).split('href="', 1)[1].split('">\n', 1)[0]
    tagline = str(article).split('title">',1)[1].split('</h3',1)[0]
    news_list.append([tagline.strip(),url.strip()])


content = random.choice(news_list)


with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

nsec = config['nsec']

private_key = PrivateKey().from_nsec(nsec)
public_key = private_key.public_key

relay_manager = RelayManager()
relay_manager.add_relay("wss://nostr-pub.wellorder.net")
relay_manager.add_relay("wss://relay.damus.io")
relay_manager.add_relay("wss://nos.lol")
relay_manager.add_relay("wss://nostr.zebedee.cloud")
relay_manager.add_relay("wss://nostr.bitcoiner.social")
relay_manager.add_relay("wss://nostr.stoner.com")
relay_manager.add_relay("wss://relay.nostr.info")
relay_manager.add_relay("wss://relay.mostr.pub")
relay_manager.add_relay("wss://offchain.pub")
relay_manager.add_relay("wss://relay.utxo.one")
relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
time.sleep(10) # allow the connections to open

note = content[0] + '\n' + content[1]
event = Event(public_key = public_key.hex(), content = note)
private_key.sign_event(event)
try:
    relay_manager.publish_event(event)
finally:
    time.sleep(60) # allow the messages to send
    relay_manager.close_connections()