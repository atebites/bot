import os
import discord
from discord.ext import commands

################################################################################

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

################################################################################

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(status=discord.Status.online)

#@bot.event
#async def on_message(message):
#    if message.author == bot.user:
#        return
#    if message.content.startswith("!hello"):
#        await message.channel.send("Hello!")

################################################################################

@bot.command()
async def restart(ctx):
    if str(ctx.author.id) != os.getenv("ADMIN_ID"):
        await ctx.send(f"Your ID '{str(ctx.author.id)}' does not have permission to run this command.")
        return
    await ctx.send(f"Restarting bot...")
    await bot.close()
    os.execv(sys.executable, ["python"] + sys.argv)
    os._exit(1)

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

################################################################################

bot.run(os.getenv("TOKEN"))
