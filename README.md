# Fuccbot
#### A stupid discord bot

## What is it?
 Fuccbot (apparently pronounced "fuss-bot") is essentially
a customizable jester using the [discord python library](https://github.com/Rapptz/discord.py).
My friends and I wanted a discord bot we could program our own sound clips and other
silly stuff into, so I made one for us.

You can program "memes" into it--a text response, a tts response, or a sound
clip--and create variants of each "meme" if you want it to do more than one for
a given command.

Currently, the application is only made to connect to and provide services to a
single server. There is potential, with light modification, for it to support multiple
servers.

## How do I make it work?

### How to add a meme

Memes are added in `config.py`. They are first defined, then added to the list
`config.BOT_MEMES`

In `fuccbot.memes` you'll find a simple base `Meme` class and a few wrapper subclasses.
Right now, the only thing the wrapper subclasses do is provide a unique class that
can be singled out if necessary, and set the `type` property to something other
than `'none'` (this is mostly only useful for the help command)

A meme requires a main "command" it can be bound to. This is the first argument
supplied:

    from fuccbot.memes import TextMeme

    hello = TextMeme('hello')

A meme may optionally have an unlimited number of aliases associated with it:

    from fuccbot.memes import TextMeme

    hello = TextMeme('hello', 'hw')

Aliases can be assigned and added after creation:

    hello = TextMeme('hello')
    hello.aliases = ['greet']
    hello.aliases.append('hw')

#### How to add a meme variant

Unless you provide at least one variant to a given meme, it won't do anything.
Variants are added to a meme using the `@meme.variant` decorator:

    import asyncio
    from fuccbot.memes import TextMeme

    @hello.variant('hello')
    async def hello_default(meme, client, message):
        text = 'Hello, World!'
        return await client.send_message(message.channel, text)

The variant is named by the string passed to `@meme.variant()` and the decorated
function must accept three positional arguments:

1. `meme` -- When the meme calls the decorated function, it will pass itself in.
2. `client` -- The `discord.Client` instance the bot is using
3. `message` -- The `discord.Message` that triggered this meme

#### A complete example using all three wrappers:

    import asyncio
    import discord
    import logging
    import os.path
    from fuccbot.memes import SoundMeme, TextMeme, TTSMeme

    logger = logging.getLogger('discord')

    soundboard = SoundMeme('soundboard', 'board')
    hello = TextMeme('hello', 'hw')
    robot = TTSMeme('robot')


    async def play_sound(filename, meme, client, message):
        file_path = os.path.join(os.path.dirname(__file__), 'sounds', filename)
        voice_channel = message.author.voice_channel
        if voice_channel is not None:
            voice = await client.join_voice_channel(voice_channel)
            try:
                player = voice.create_ffmpeg_player(filepath)
                player.start()
                while player.is_playing():
                    pass
                await voice.disconnect()
            except discord.ClientException as e:
                logger.error(e)
                await voice.disconnect()


    # May decorate the same function multiple times to alias variants
    @soundboard.variant('sad')
    @soundboard.variant('sadtrombone')
    async def soundboard_sad(meme, client, message):
        return await play_sound('sadtrombone.wav', meme, client, message)


    @soundboard.variant('fail')
    @soundboard.variant('failtuba')
    async def soundboard_fail(meme, client, message):
        return await play_sound('failtuba.wav', meme, client, message)


    @soundboard.variant('rim')
    @soundboard.variant('rimshot')
    async def soundboard_rim(meme, client, message):
        return await play_sound('rimshot.wav', meme, client, message)


    @hello.variant('hello')
    async def hello_default(meme, client, message):
        text = 'Hello, World!'
        return await client.send_message(message.channel, text)


    @hello.variant('hi')
    async def hello_hi(meme, client, message):
        text = 'Hi, {0}!'.format(message.author.name)
        return await client.send_message(message.channel, text)


    @robot.variant('beep')
    async def robot_beep(meme, client, message):
        text = 'I am a robot. Beep boop.'
        return await client.send_message(message.channel, text, tts=True)


    @robot.variant('jobs')
    async def robot_beep(meme, client, message):
        text = 'I am a robot. I run on American jobs.'
        return await client.send_message(message.channel, text, tts=True)

## How to run the bot

**Requirements:**

* Python 3.5 or greater
* ffmpeg (for `SoundMeme`)
* [discord python library](https://github.com/Rapptz/discord.py) (and its requirements)
in your python path.

It is recommended to run this in a virtualenv. If you don't know how to do that,
[this handy guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/) might help.

Once you have your Python 3.5 installation and the discord library in your environment
(virtual or otherwise,) place `fuccbot` and `config.py` in a desired location. You should
 edit `config.py` to your liking (see "Configuration Options" below) and then you may run
 the bot by typing `python client.py` into your command line interface (don't
 forget to activate your virtualenv if you created one!)

## How to use the bot

The bot will automatically read and register all memes from `config.BOT_MEMES`. Memes
may be summoned from discord text chat using the `!fuccbot` or `!fb` commands. There
is a special builtin subcommand, `!fuccbot help` which may also be used as `!fuccbot h`,
`!fb help`, and `!fb h`

The standard syntax to summon a meme is `!fuccbot <meme> <variant>` where:

* `<meme>` is a command or alias for a meme created in `config.py` and added to
`config.BOT_MEMES`
* `<variant>` is the name of a meme variant as supplied to the `@meme.variant()` decorator

Using the previous complete code example, someone can call upon the bot to play a
"Sad Trombone" noise in their voice channel by typing `!fuccbot soundboard sadtrombone`
into chat. Alternatively, they could type `!fb board sad` for something shorter and
quicker to type. If they didn't care what noise played, they could just type
`!fuccbot soundboard`, `!fb board`, `!fuccbot board`, etc. and a random noise would
play.

If there are multiple variants registered to a meme and:
* a variant is not supplied
***or***
* a variant name is supplied but is not found to be associated with the variants
for that meme

the bot will pick a random variant and trigger it.

## Configuration Options

* `BOT_TOKEN` -- Your discord bot's token. It can be found in
[your applications](https://discordapp.com/developers/applications/me). Keep it secret!
* `BOT_LISTENS_TO_ROLES` -- A list of user role names to listen to. If this is empty,
the bot will listen to everybody. If this has anything in it, the bot will only listen
to users who have roles that match. Be sure to spell the role names correctly!
* `BOT_LISTENS_TO_CHANNELS` -- A list of text channel names to listen to. If this is empty,
the bot will listen to all channels it has permission to see. If this has anything in it,
the bot will only listen to channels that match. Be sure to spell the channel names correctly!
* `BOT_MEMES` -- A list of memes the bot supports. See "How to add a meme" above.

## Changelog

**0.0.1** - initial