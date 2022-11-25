import os
import discord
from discord.ext import commands
import random

################################################################################

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix="!", intents=intents)

################################################################################

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(status=discord.Status.online)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    #if message.content.startswith("!hello"):
    #    await message.channel.send("Hello!")
    await bot.process_commands(message)

#@bot.event
#async def on_reaction_add(reaction, user):
#    if message.author == bot.user:
#        return
#    # Get the location of the reaction.
#    channel = await bot.fetch_channel(reaction.message.channel.id)
#    message = await channel.fetch_message(reaction.message.id)
#    # Remove the reaction.
#    await reaction.remove(user)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing command arguments.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have permission to use use this command")

################################################################################

@bot.command(brief="Restart the bot.", description="To allow for easy updates this command can be used to turn the bot off and on again.")
async def restart(ctx):
    if str(ctx.author.id) != os.getenv("ADMIN_ID"):
        await ctx.reply(f"Your ID '{str(ctx.author.id)}' does not have permission to run this command.")
        return
    await ctx.reply(f"Restarting bot...")
    await bot.close()
    os.execv(sys.executable, ["python"] + sys.argv)
    os._exit(1)

@bot.command(brief="Ping-Pong test command.", description="This is a simple test command to check things are working. When you say 'ping', the bot will say 'pong'.")
async def ping(ctx):
    await ctx.send("pong")

################################################################################

@bot.command(brief="Play a game.", description="Launch a game as specified by the argument. Currently only rock-paper-scissors (rps) is supported.")
async def game(ctx, game):
    if not game in games:
        await ctx.reply(f"Sorry {ctx.author.name} I don't know that game")
        return
    await games[game](ctx)
    
@bot.command(brief="Enter a move for a game.", description="When playing a game use this command to play a move.")
async def move(ctx, move):
    if not ctx.author.id in players:
        await ctx.reply(f"You aren't playing any games {ctx.author.name}???")
        return
    game = players[ctx.author.id]
    if not move in moves[game]:
        await ctx.reply(f"Sorry {ctx.author.name} I don't know that move for {game}.")
        return
    await play[game](ctx, move)
    
async def clear_game(ctx):
    if not ctx.author.id in players:
        await ctx.reply(f"You aren't playing any games {ctx.author.name}???")
        return
    game = players[ctx.author.id]
    await ctx.reply(f"Clearing the current game of {game} for you {ctx.author.name}.")
    del players[ctx.author.id]

async def setup_rock_paper_scissors(ctx):
    players[ctx.author.id] = "rock-paper-scissors"
    await ctx.reply(f"Ready when you are {ctx.author.name}. Use one of: '!move rock'/'!move paper'/'!move scissors'.")

async def play_rock_paper_scissors(ctx, move):
    move_bot = random.choice(["rock", "paper", "scissors"])
    if move == move_bot:
        await ctx.reply(f"It's a tie {ctx.author.name}. We both chose {move}.")
    elif (move == "rock" and move_bot == "paper") or (move == "paper" and move_bot == "scissors") or (move == "scissors" and move_bot == "rock"):
        await ctx.reply(f"Victory is mine {ctx.author.name}. My {move_bot} defeats you {move}.")
    else:
        await ctx.reply(f"I am defeated {ctx.author.name}. Your {move} has overpowered my {move_bot}.")
    del players[ctx.author.id]

################################################################################

players = {
}

games = {
    "over": clear_game,
    "rock-paper-scissors": setup_rock_paper_scissors,
    "rps": setup_rock_paper_scissors,
}

moves = {
    "over": [],
    "rock-paper-scissors": ["rock", "paper", "scissors"],
}

play = {
    "over": clear_game,
    "rock-paper-scissors": play_rock_paper_scissors,
}

################################################################################

bot.run(os.getenv("TOKEN"))
