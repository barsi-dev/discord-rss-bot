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
    now = datetime.datetime.now()
    now = now.strftime("%M-%d-%Y %H:%M:%S")
    print(f"Bot started @ {now}")

@bot.command()
async def test(ctx):
    """A test command"""
    print(ctx)
    await ctx.send("test")

@bot.command()
async def manga(ctx, *, arg):
    """
    <name>
    - Asks for a name of an manga/manhwa
    - Checks Mangasee123 if manga/manhwa exists
    """
    new_arg = arg.replace("'", "").replace(".", "").replace("  ", " ").replace("(", "").replace(")", "")
    new_arg = "-".join(new_arg.split(" "))
    new_arg = "https://mangasee123.com/rss/" + new_arg + ".xml"

    print(new_arg)
    
    added = db_modules.add_to_db(db, new_arg)

    if added == 1:
        await ctx.send(f"`RSS already in list!`")
    elif added == 0:
        await ctx.send(f"`Manga/Manhwa not found on Mangasee123 database!`")
    else:
        await ctx.send(f"`Successfuly added {added} to list!`")

    print(new_arg)

@bot.command()
async def rss(ctx, *, arg):
    """<link>
    - Asks for an RSS Link
    - Watches an RSS link for updates"""
    added = db_modules.add_to_db(db, arg)

    if added == 1:
        await ctx.send(f"`RSS already in list!`")
    elif added == 0:
        await ctx.send(f"`Not a valid RSS link!`")
    else:
        await ctx.send(f"`Successfuly added {added} to list!`")

# @bot.command()
# async def help(ctx):
#     msg = f"""```
# !!rss <link>
#     - Asks for an RSS Link
#     - Watches an RSS link for updates
# !!add <name>
#     - Asks for a name of an manga/manhwa
#     - Checks Mangasee123 if manga/manhwa exists
#     ```"""

    await ctx.send(msg)

@bot.command()
async def list(ctx):
    cursor = db.cursor()
    db.commit()

    list = "Manga/Manhwa on Watchlist:\n"

    cursor.execute("SELECT latest FROM feeds ORDER BY latest ASC")
    results = cursor.fetchall()

    for latest in results:
        list = list + f"""  - {latest[0].rsplit(" ", 2)[0]}\n"""
    
    await ctx.send(f"```{list}```")
        


    cursor.close()


@bot.event
async def on_message(message):
    """Called when a Message is created and sent."""
    if message.author.bot:
        return
    await bot.process_commands(message)

bot.run(os.getenv('TOKEN'))


