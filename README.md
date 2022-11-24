# Bot #
-------

A simple discord bot.

## Commands ##

| Command | Action                  |
|--------:|:------------------------|
| $ping   | Bot responds "pong".    |

## Hosting ##

### Remote Setup ###

```
# Login.
ssh atebites@ssh-atebites.alwaysdata.net

# Initialise a bare git repository.
git init --bare ~/bot.git

# Install post-receive script.
curl -L -o ~/bot.git/hooks/post-receive https://raw.githubusercontent.com/atebites/bot/master/post-receive

# Mark it as executable.
chmod +x bot.git/hooks/post-receive
```

### Local Setup ###

```
git remote add deploy atebites@ssh-atebites.alwaysdata.net:~/bot.git
git checkout production
git push deploy production
```