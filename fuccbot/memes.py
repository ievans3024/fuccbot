import asyncio
import os
import random
import time

import discord


class Meme(object):

    def __init__(self, cmd, *aliases):
        self.command = cmd
        self.aliases = aliases
        self.type = 'none'
        self.variants = {}  # name: handler_func
        self.variant_aliases = {}  # alias: name

    def variant(self, name, *aliases):

        def decorator(f):
            if name not in self.variants:
                self.variants[name] = f
            for a in aliases:
                if a not in self.variants and a not in self.variant_aliases:
                    self.variant_aliases[a] = name
            return f
        return decorator

    @property
    def help(self):
        main_text = '!fuccbot ' + self.command
        type_text = 'Type: {0}'.format(self.type)
        alias_text = ''
        variant_text = ''
        if len(self.variants) > 1:
            main_text += ' [<variant>]'
            variant_text = 'Variants: \n  '
            variants = []
            for k in self.variants:
                aliases = [alias for alias, name in self.variant_aliases.items() if name == k]
                variants.append('{0} (aliases: {1})'.format(k, ', '.join(aliases)))
            variant_text += '\n  '.join([v for v in variants])
        if len(self.aliases):
            alias_text = 'Aliases: '
            alias_text += ', '.join([a for a in self.aliases])
        text_nodes = ['', main_text, '', type_text]
        if len(alias_text):
            text_nodes.append('')
            text_nodes.append(alias_text)
        if len(variant_text):
            text_nodes.append('')
            text_nodes.append(variant_text)
        return '\n  '.join(text_nodes)

    async def do(self, client, message, variant=None):

        def pick_random():
            h = random.choice(list(self.variants.keys()))
            return self.variants[h]

        if variant is None:
            handler = pick_random()
        elif self.variants.get(variant) is None:
            # try aliases
            if self.variant_aliases.get(variant) is None:
                handler = pick_random()
            else:
                name = self.variant_aliases[variant]
                handler = self.variants[name]
        else:
            handler = self.variants[variant]

        return await handler(self, client, message)


class SoundMeme(Meme):

    def __init__(self, cmd, *aliases, sounds_dir=os.path.dirname(__file__)):
        super(SoundMeme, self).__init__(cmd, *aliases)
        self.type = 'sound'
        self.sounds_dir = sounds_dir

    @staticmethod
    async def leave_all_voices(client):
        voices = list(client.voice_clients)
        while len(voices):
            await client.voice_clients[0].disconnect()

    @staticmethod
    async def join_voice_channel(client, channel):
        return await client.join_voice_channel(channel)

    @staticmethod
    async def leave_voice_channel(voice_client):
        return await voice_client.disconnect()

    async def play_sound(self, filename, voice_client):
        filepath = os.path.join(self.sounds_dir, filename)
        try:
            player = voice_client.create_ffmpeg_player(filepath)
            player.volume = 1.0
            player.start()
            while player.is_playing():
                time.sleep(0.1)
        except discord.ClientException as e:
            print(e)
        finally:
            return None

    def variant(self, name, *aliases, filename=None):
        def decorator(f):
            if name not in self.variants:
                self.variants[name] = f
            for a in aliases:
                if a not in self.variant_aliases:
                    self.variant_aliases[a] = name
            f.filename = filename
            return f
        return decorator


class TextMeme(Meme):

    def __init__(self, cmd, *aliases):
        super(TextMeme, self).__init__(cmd, *aliases)
        self.type = 'text'


class TTSMeme(Meme):

    def __init__(self, cmd, *aliases):
        super(TTSMeme, self).__init__(cmd, *aliases)
        self.type = 'tts'
