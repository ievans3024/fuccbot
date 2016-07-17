import asyncio
from fuccbot.memes import TextMeme

# -- Meme definitions --
hello = TextMeme('hello')


@hello.variant('hello')
async def hello_default(meme, client, message):
    text = 'Hello, World!'
    return await client.send_message(message.channel, text)


@hello.variant('hi')
async def hello_hi(meme, client, message):
    text = 'Hi, {0}!'.format(message.author.name)
    return await client.send_message(message.channel, text)

# -- Login info --
# Bot token
BOT_TOKEN = ''


# -- Bot behavior --

# List of role names the bot will listen to (empty for anybody)
# Bot will not listen to anyone if roles are specified here that don't exist!
BOT_LISTENS_TO_ROLES = []

# List of text channel names the bot should pay attention to (empty for all channels)
# Bot will not listen to any channels if channels are specified here that don't exist!
BOT_LISTENS_TO_CHANNELS = []

# List of memes the bot handles
BOT_MEMES = [hello]
