import discord
from discord.ext import commands
import os
import random
from replit import db
from utils.Cooldown import Cooldown


intents = discord.Intents.default()
client = discord.Client(intents=intents)
PREFIX = "dw!"

def checkIfUserExists(author):
  try:
    db[str(author)]
  except:
    db[str(author)] = {
      "coins": 10,
    }

bot = commands.Bot(command_prefix = PREFIX, intents=intents)


@client.event
async def on_ready():
  print(f"Bot logged in as {client.user}")
  await bot.change_presence(activity=discord.Game(name="dw!help"))


@client.event
async def on_message(Msg):
  if Msg.author == client.user:
    return
  msg = Msg.content
  
  if msg.startswith(f"{PREFIX}help"):
    builder = discord.Embed(title = "Discwordle commands", name = "Help", description = f"""`{PREFIX}help`: Helps with bot commands.
`{PREFIX}dgame`: Play the daily Wordle game.""")
    await Msg.channel.send(embed = builder)

  if msg.startswith(f"{PREFIX}game"):
    checkIfUserExists(msg.author.id)
    cooldown = Cooldown()
    cooldown.get_ratelimit(Msg)
    print(await cooldown.check(Msg))
    game_choice = random.randint(1, 2)
    if game_choice == 1 or game_choice == 2: # Change this when there are more games
      game = EmojiGame(msg,   client)
      await game.run_game()
      isCorrectEmoji = game.get_info()
      if game.is_done():
        await game.emj_msg.clear_reactions()
        if isCorrectEmoji:
          await game.emj_msg.edit(content = f"{msg.author.mention}, you had the correct emoji! You got 1000 Mora!")
          db[str(msg.author.id)]["mora"] += 1000
        else:
          await game.emj_msg.edit(content = f"{msg.author.mention}, you had the wrong emoji!")
        game.reset() # Resets all of the variables for cleanup and easy memory destruction
    

client.run(os.environ["TOKEN"])