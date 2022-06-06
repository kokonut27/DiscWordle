import discord
from discord.ext import commands
import os
import random
from replit import db
from utils.Cooldown import Cooldown


intents = discord.Intents.default()
client = discord.Client(intents=intents)
PREFIX = "dw!"
activity = discord.Game(name = "dw!help")

def checkIfUserExists(author):
  try:
    db[str(author)]
  except:
    db[str(author)] = {
      "coins": 10,
    }

for all in db.keys():
  print(all)

bot = commands.Bot(command_prefix = PREFIX, activity=activity, intents=intents)


@client.event
async def on_ready():
  await client.change_presence(activity=activity)
  print(f"Bot logged in as {client.user}")


@client.event
async def on_message(Msg):
  if Msg.author == client.user:
    return
  msg = Msg.content

  if msg.startswith(f"{PREFIX}help"):
    builder = discord.Embed(title = "DiscWordle commands", name = "Help", description = f"""`{PREFIX}help`: Helps with bot commands.
`{PREFIX}dgame`: Play the daily Wordle game.""")
    await Msg.channel.send(embed = builder)

  if msg.startswith(f"{PREFIX}dgame"):
    checkIfUserExists(Msg.author.id)
    cooldown = Cooldown()
    cooldown.get_ratelimit(Msg)
    print(await cooldown.check(Msg))
    await Msg.channel.send(content = "hi :D")
    
client.run(os.environ["TOKEN"])