import os
import discord
import mysql.connector
from discord.ext import commands
from dotenv import load_dotenv
from pprint import pprint
from time import sleep
import datetime

import db_modules

load_dotenv()

db = mysql.connector.connect(
  host=os.getenv('HOST'),
  user=os.getenv('USER'),
  password=os.getenv("PASS"),
  database=os.getenv("DB")
)

# Intents are new in version 1.5.
bot = commands.Bot(command_prefix='!!', intents=discord.Intents.all())



@bot.event
async def on_ready():
    """Called when the client is done preparing the data received from Discord."""
    print("Bot is ready")

    channel = bot.get_channel(int(os.getenv("CHANNEL")))
    print(channel)
    i = 1
    cursor = db.cursor()

    while 1:
        db.commit()
        cursor = db.cursor()
        cursor.execute("SELECT link, latest FROM feeds")
        now = datetime.datetime.now()
        now = now.strftime("%m-%d-%Y %H:%M:%S")
        print(f"[{i}] {now}")
        i +=1

        db_result = cursor.fetchall()

        for row in db_result:
            is_latest = db_modules.is_latest(row)

            if not is_latest:
                latest_chapters = db_modules.get_latest_chapters(db, row)
            
                for chapter in latest_chapters[::-1]:
                    title = chapter["title"].rsplit(" ", 2)[0].replace("'", "").replace(".", "").replace("  ", " ").title()
                    new_arg = "-".join(title.split(" "))
                    image_link = "https://cover.nep.li/cover/" + new_arg +".jpg"
                    print(image_link)

                    embed_text = discord.Embed()
                    embed_text.title = chapter["title"]
                    embed_text.url = chapter["link"]
                    embed_text.colour = 0x3498db
                    embed_text.set_author(name=f"New {title} chapter!")
                    embed_text.set_thumbnail(url=image_link)
                    await channel.send("<@&772429737724346370>")
                    await channel.send(embed=embed_text)

                    print(f"New release for {title}!")
        sleep(60)
        cursor.close()


bot.run(os.getenv('TOKEN'))


