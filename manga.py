from time import sleep
from pprint import pprint
import feedparser


class Mangasee:
    def __init__(self, link):
        self.link = link
        latest = feedparser.parse(link)
        self.latest = latest.entries[0].title

    def checkNew(self):
        feed = feedparser.parse(self.link)
        for entry in feed.entries:
            if(entry.title == self.latest):
                print("No updates yet!")
                return

            print("\n")
            print(entry.title)
            print(entry.link)
            self.latest = entry.title
            return


rss = Mangasee("https://www.youtube.com/feeds/videos.xml?channel_id=UCw-Q-wTBw9NC4X8QsZAueeA")


a = "test"


            