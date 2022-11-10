import os
import discord
from discord.ext import commands

################################################################################

intents = discord.Intents.default()
intents.message_content = True

#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)

################################################################################

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

#@bot.event
#async def on_message(message):
#    if message.author == bot.user:
#        return
#    if message.content.startswith('$hello'):
#        await message.channel.send('Hello!')

################################################################################

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

################################################################################

bot.run(os.getenv('TOKEN'))
