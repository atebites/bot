import os
import discord
from discord.ext import commands
import random
from english_words import english_words_lower_set

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
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing command arguments.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have permission to use use this command")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("Command invoke error.")
        raise error
    else:
        await ctx.send("Unknown error.")
        raise error

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
    game = game.lower()
    if game != "over" and ctx.author.id in players:
        await ctx.reply(f"You're already playing a game {ctx.author.name}. End your current game of {players[ctx.author.id]['game']} with the command `!game over`.")
        return
    if not game in games:
        await ctx.reply(f"Sorry {ctx.author.name} I don't know that game.")
        return
    await games[game](ctx)
    
@bot.command(brief="Enter a move for a game.", description="When playing a game use this command to play a move.")
async def move(ctx, move):
    if not ctx.author.id in players:
        await ctx.reply(f"You aren't playing any games {ctx.author.name}. Start a game with the `!game` command.")
        return
    game = players[ctx.author.id]["game"]
    move = move.lower()
    if not move in moves[game]:
        await ctx.reply(f"Sorry {ctx.author.name} I don't know that move for {game}.")
        return
    await play[game](ctx, move)
    
async def clear_game(ctx):
    if not ctx.author.id in players:
        await ctx.reply(f"You aren't playing any games {ctx.author.name}, so nothing to clear.")
        return
    game = players[ctx.author.id]["game"]
    await ctx.reply(f"Clearing the current game of {game} for you {ctx.author.name}.")
    del players[ctx.author.id]

async def setup_rock_paper_scissors(ctx):
    players[ctx.author.id] = {}
    players[ctx.author.id]["game"] = "rock-paper-scissors"
    await ctx.reply(f"Ready when you are {ctx.author.name}. Use one of: '!move rock' / '!move paper' / '!move scissors'.")

async def play_rock_paper_scissors(ctx, move):
    move_bot = random.choice(["rock", "paper", "scissors"])
    if move == move_bot:
        await ctx.reply(f"It's a tie {ctx.author.name}. We both chose {move}.")
    elif (move == "rock" and move_bot == "paper") or (move == "paper" and move_bot == "scissors") or (move == "scissors" and move_bot == "rock"):
        await ctx.reply(f"Victory is mine {ctx.author.name}. My {move_bot} defeats you {move}.")
    else:
        await ctx.reply(f"I am defeated {ctx.author.name}. Your {move} has overpowered my {move_bot}.")
    del players[ctx.author.id]

HANGMAN_STAGES = [
    "  +---+ \n      | \n      | \n      | \n========\n", 
    "  +---+ \n  O   | \n      | \n      | \n========\n", 
    "  +---+ \n  O   | \n  |   | \n      | \n========\n", 
    "  +---+ \n  O   | \n /|   | \n      | \n========\n", 
    "  +---+ \n  O   | \n /|\  | \n      | \n========\n", 
    "  +---+ \n  O   | \n /|\  | \n /    | \n========\n", 
    "  +---+ \n  O   | \n /|\  | \n / \  | \n========\n"
]

async def setup_hangman(ctx):
    players[ctx.author.id] = {}
    players[ctx.author.id]["game"] = "hangman"
    players[ctx.author.id]["word"] = random.choice(list(english_words_lower_set))
    players[ctx.author.id]["letters_guessed"] = []
    players[ctx.author.id]["letters_missed"] = []
    word_blank = " ".join(["_"] * len(players[ctx.author.id]["word"]))
    await ctx.reply(f"Ready when you are {ctx.author.name}. Enter letters using: '!move letter' e.g. `!move a`.")
    await ctx.reply("```" + HANGMAN_STAGES[0] + "```")
    await ctx.reply("`" + word_blank + "`")
    

async def play_hangman(ctx, move):
    if move in players[ctx.author.id]["letters_guessed"] or move in players[ctx.author.id]["letters_missed"]:
        await ctx.reply(f"You have already guessed that letter {ctx.author.name}. Choose again.")
        return
        
    if move in players[ctx.author.id]["word"]:
        players[ctx.author.id]["letters_guessed"].append(move)
    else:
        players[ctx.author.id]["letters_missed"].append(move)
    
    word_blank = " ".join(["_"] * len(players[ctx.author.id]["word"]))
    for i in range(len(players[ctx.author.id]["word"])):
        if players[ctx.author.id]["word"][i] in players[ctx.author.id]["letters_guessed"]:
            word_blank = word_blank[:(i*2)] + players[ctx.author.id]["word"][i] + word_blank[(i*2)+1:]
        
    if "_" not in word_blank:
        await ctx.reply(f"I am defeated {ctx.author.name}. You guessed my word `{' '.join(players[ctx.author.id]['word'])}` with only {len(players[ctx.author.id]['letters_missed'])} mistakes.")
        del players[ctx.author.id]
        return
        
    await ctx.reply("Misses: " + " ".join(players[ctx.author.id]["letters_missed"]))
    await ctx.reply("```" + HANGMAN_STAGES[len(players[ctx.author.id]["letters_missed"])] + "```")
    await ctx.reply("`" + word_blank + "`")
    
    if len(players[ctx.author.id]["letters_missed"]) == 6:
        await ctx.reply(f"Victory is mine {ctx.author.name}. You failed to guess the word `{' '.join(players[ctx.author.id]['word'])}`.")
        del players[ctx.author.id]
    
################################################################################

players = {
    # ctx.author.id : {
    #     "game" : "name-of-game,
    #     "XXX"  : "other-game-state-values..."
    # },
}

games = {
    "over": clear_game,
    "rock-paper-scissors": setup_rock_paper_scissors,
    "rps": setup_rock_paper_scissors,
    "hangman": setup_hangman,
}

moves = {
    "over": [],
    "rock-paper-scissors": ["rock", "paper", "scissors"],
    "hangman": ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
}

play = {
    "over": clear_game,
    "rock-paper-scissors": play_rock_paper_scissors,
    "hangman": play_hangman,
}

################################################################################

bot.run(os.getenv("TOKEN"))
