import asyncio
import config
import discord
import discord.utils
import logging

import fuccbot.bot

client = discord.Client()
bot = fuccbot.bot.Bot(config.BOT_TOKEN, client)


@client.event
async def on_ready():
    servers = list(client.servers)
    if len(servers):
        server = servers[0]

        # get channels to listen to
        channels = [c for c in server.channels if c.type == discord.ChannelType.text]
        if len(config.BOT_LISTENS_TO_CHANNELS):
            channels = [c for c in server.channels if c.name in config.BOT_LISTENS_TO_CHANNELS]
        bot.channels += channels

        # get roles to listen to
        if len(config.BOT_LISTENS_TO_ROLES):
            bot.roles = [r for r in server.roles if r.name in config.BOT_LISTENS_TO_ROLES]
        else:
            bot.roles = [discord.utils.find(lambda x: x.name == '@everyone', server.roles)]

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.channel in bot.channels:
        member = message.author
        if member.id != bot.client.user.id:
            if any([r for r in member.roles if r in bot.roles]):
                message_parts = message.content.split(' ')
                if message_parts[0] in {'!fuccbot', '!fb'}:
                    await bot.do_meme(message, message.channel)

if __name__ == '__main__':
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    bot.register_memes(*config.BOT_MEMES)
    client.run(bot.token)
