import discord
from discord.ext import commands
import os
import random
import sqlite3
from replit import db
from utils.Cooldown import Cooldown
from utils.Words import getWord


def get_db_connection():
  conn = sqlite3.connect('DiscWordle/utils/database/database.db')
  conn.row_factory = sqlite3.Row
  return conn

def getWordle():
  conn = get_db_connection()
  max = conn.execute('SELECT *, max(id) FROM wordles').fetchone()["id"]
  min = conn.execute('SELECT *, min(id) FROM wordles').fetchone()["id"]
  _id = random.randint(min, max)
  wordle = conn.execute('SELECT * FROM wordles WHERE id = ?', (_id, )).fetchone() 
  conn.close()
  
  return wordle

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

# db.clear()

bot = commands.Bot(command_prefix = PREFIX, activity=activity, intents=intents)
allCommands = [
  "dw!help",
  "dw!dgame",
  "dw!game"
]

@client.event
async def on_ready():
  await client.change_presence(activity=activity)
  print(f"Bot logged in as {client.user}")


@client.event
async def on_message(Msg):
  msg = Msg.content
  if Msg.author == client.user:
    return
  elif str(Msg.author.id) not in db.keys():
    if msg in allCommands:
      builder = discord.Embed(title = "Welcome!", name = "Welcome", color=0x6aaa64, description = f"Hey {Msg.author.mention}, seems like you're a new user to DiscWordle! Glad to have you with us, and if you need any help, just type `dw!help`. \n\nEnjoy!")
      # await Msg.channel.send(embed = builder)
      await Msg.reply(embed = builder, mention_author=True)
      checkIfUserExists(Msg.author.id) # Creates user

  if msg.startswith(f"{PREFIX}help"):
    builder = discord.Embed(title = "DiscWordle commands", name = "Help", color=0x6aaa64, description = f"""`{PREFIX}help`: Helps with bot commands.
`{PREFIX}dgame`: Play the official daily Wordle game.
`{PREFIX}game`: Play a custom Wordle game.
`{PREFIX}multigame`: Play a multiplayer Wordle game with your friends!""")
    await Msg.channel.send(embed = builder)

  if msg.startswith(f"{PREFIX}dgame"):
    checkIfUserExists(Msg.author.id)
    cooldown = Cooldown()
    cooldown.get_ratelimit(Msg)
    print(await cooldown.check(Msg))
    await Msg.channel.send(content = "hi :D")

  if msg.startswith(f"{PREFIX}game"):
    checkIfUserExists(Msg.author.id)
    cooldown = Cooldown()
    cooldown.get_ratelimit(Msg)
    print(await cooldown.check(Msg))

    # 
    
try:
  client.run(os.environ["TOKEN"])
except discord.errors.HTTPException:
  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
  os.system("python DiscWordle/utils/restart.py")
  os.system('kill 1')