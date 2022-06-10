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
topics = ["gaming", "fun", "music", "general", "math", "science", "english", "history", "school"]

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
  if str(Msg.author.id) not in db.keys():
    if msg in allCommands:
      builder = discord.Embed(title = "Welcome!", name = "Welcome", color=0x6aaa64, description = f"Hey {Msg.author.mention}, seems like you're a new user to DiscWordle! Glad to have you with us, and if you need any help, just type `dw!help`. \n\nEnjoy!")
      # await Msg.channel.send(embed = builder)
      await Msg.reply(embed = builder, mention_author=True)
      checkIfUserExists(Msg.author.id) # Creates user

  if msg.startswith(f"{PREFIX}help"):
    builder = discord.Embed(title = "DiscWordle commands", name = "Help", color=0x6aaa64, description = f"""`{PREFIX}help`: Helps with bot commands.
`{PREFIX}dgame`: Play the official daily Wordle.
`{PREFIX}game [id]`: Play a random community Wordle. Optional: [id] chooses a specific community Wordle to play.
`{PREFIX}guess [word] [id]`: Guess a word in any Wordle. Only works once you have started. [id]: Enter the Wordle id you're guessing for.
`{PREFIX}multigame`: Play a multiplayer Wordle with your friends!
`{PREFIX}allgames`: Look at all Wordles available that are made by the community!
`{PREFIX}create [word] [topic]`: Create a Wordle and post it to the community.""")
    await Msg.channel.send(embed = builder)

  if msg.startswith(f"{PREFIX}dgame"):
    checkIfUserExists(Msg.author.id)
    cooldown = Cooldown()
    cooldown.get_ratelimit(Msg)
    print(await cooldown.check(Msg))
    await Msg.channel.send(content = "hi :D")

  if msg.startswith(f"{PREFIX}guess"):
    checkIfUserExists(Msg.author.id)
    cooldown = Cooldown()
    cooldown.get_ratelimit(Msg)
    print(await cooldown.check(Msg))

    message = msg.split()
    letterGuess = message[1]
    wordleId = message[2]

  if msg.startswith(f"{PREFIX}create"):
    checkIfUserExists(Msg.author.id)
    cooldown = Cooldown()
    cooldown.get_ratelimit(Msg)
    print(await cooldown.check(Msg))

    message = msg.split()
    word = message[1]
    topic = message[2]

    if len(word) == 5:
      if word in getWord():
        if topic.lower() in topics:
          conn = get_db_connection()
          conn.execute("INSERT INTO wordles (creator, word, topic) VALUES (?, ?, ?)", (Msg.author.id, word, topic))
          conn.commit()
          conn.close()
          
          id = getWordle()["id"]
          empty = "⬜"

          builder = discord.Embed(title = f"Wordle created! | Wordle #{str(id)}", name = "Wordle created", color=0x6aaa64, description = f"""> **Created by: <@{Msg.author.id}> | Topic: {topic}**

{empty*5}
{empty*5}
{empty*5}
{empty*5}
{empty*5}
{empty*5}""")
          await Msg.channel.send(embed = builder)
        else:
          builder = discord.Embed(title = "Topic doesn't exist!", name = "No topic", color=0x6aaa64, description = f"`{topic}` does not exist!")
          await Msg.channel.send(embed = builder)
      else:
        builder = discord.Embed(title = "Word doesn't exist!", name = "No word", color=0x6aaa64, description = f"`{word}` is not a word that is in the dictionary!")
        await Msg.channel.send(embed = builder)
    else:
      builder = discord.Embed(title = "Word isn't 5 letters!", name = "Not five letters", color=0x6aaa64, description = f"`{word}` is not a 5 letter word!")
      await Msg.channel.send(embed = builder)

  if msg.startswith(f"{PREFIX}game"):
    checkIfUserExists(Msg.author.id)
    cooldown = Cooldown()
    cooldown.get_ratelimit(Msg)
    print(await cooldown.check(Msg))

    wordle = getWordle()
    topic = wordle["topic"]
    id = wordle["id"]
    word = wordle["word"]
    creator = wordle["creator"]
    nonexist = "⬛"
    correct = "🟩"
    incorrect = "🟨"
    empty = "⬜"
    guesses = 5
    
    builder = discord.Embed(title = f"Wordle #{str(id)}", name = "Community Wordle", color=0x6aaa64, description = f"""> **Created by: <@{creator}> | Topic: {topic}**

{empty*5}
{empty*5}
{empty*5}
{empty*5}
{empty*5}
{empty*5}""")
    await Msg.channel.send(embed = builder)
    
try:
  client.run(os.environ["TOKEN"])
except discord.errors.HTTPException:
  print("Resetting due to rate limits.")
  os.system("python DiscWordle/utils/restart.py")
  os.system('kill 1')