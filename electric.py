import requests
import lxml
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed # best working module for webhooks in my experience
import time # sleep() function for loop
from datetime import datetime # gets current date for webhook
import numpy as np
import random


headers = {
    'authority': 'www.crawfordelectricsupply.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
}



class Electric():
    def __init__(self):
        self.s = requests.Session() # first variable used in classes
        self.responseSoup = "" # current responseSoup
        self.title = "" # current title
        self.webhook = "" # current discord webhook

    def sendDiscordWebhook(self, title, sku):
        # Input whatever webhook you'd like in between the "" in the DiscordWebhook function
        webhook = DiscordWebhook(self.webhook)

        # All fields used in the webhook, can change/ add more or less
        embed = DiscordEmbed(title = (title), url = f"https://www.crawfordelectricsupply.com/product/detail/{sku}/")
        embed.set_timestamp()
        #embed.set_thumbnail(url = (image))
        embed.add_embed_field(name ="SKU", value = (sku))

        # Final execution
        try:
            webhook.add_embed(embed)
            webhook.execute()
        except:
            print("No webhook specifed!") # If user doesn't enter a webhook URL

    def getResponse(self, title, webhook): # Gets a basic response from a webpage, and parses accordingly to lxml
        self.webhook = webhook # Updates webhook

        response = self.s.get(f"https://www.crawfordelectricsupply.com/product/search?q={title}&size=108", headers = headers)
        self.responseSoup = BeautifulSoup(response.text, "lxml") # parses text from response
        self.getProduct(title)


    def getProductTitle(self, SKU):
        titleFind = self.responseSoup.find("div", {"data-product-id": f"{SKU}"})
        titleFind = titleFind.find("div", {"class": "mt5"})["data-analytics-description"]

        return titleFind


    def getProduct(self, title):
        stockFind = self.responseSoup.findAll("span", {"class": "checkStock btn-link"}) # finds instock product based on "Check your local branch" field.

        for i in stockFind: # Splits the found stock by data-id/SKU
            sku = i["data-id"]
            title = self.getProductTitle(i["data-id"])

            print("Found product! : " + str(title) + (f"\nLink : https://www.crawfordelectricsupply.com/product/detail/{sku}/")) 
            self.sendDiscordWebhook(title, sku)





######### Change the below fields ######### 

# Enter your webhook for your discord here
webhook = ""

# Syntax : ["<entry>"] 
# or for multiple entries, Syntax : ["<entry>", <"entry">] 
# Just make sure you add a comma and "" between entries
title = ["siemens wmm3", "siemens wmm4", "siemens wmm5", "siemens wmm6"]

# Minutes to sleep between loops, default 60
minutesSleep = 60






# Don't change the below #

randomNums = [3, 5, 7, 11]

while (True): 
    for i in title:
        Electric().getResponse(i, webhook)

    time.sleep((minutesSleep - random.choice(randomNums)) * 60)
