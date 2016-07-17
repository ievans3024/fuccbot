import asyncio
import random


class Meme(object):

    def __init__(self, cmd, *aliases):
        self.command = cmd
        self.aliases = aliases
        self.type = 'none'
        self.variants = {}

    def variant(self, name):

        def decorator(f):
            self.variants[name] = f
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
            variant_text = 'Variants: '
            variant_text += ', '.join([v for v in self.variants])
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
        if variant is None or self.variants.get(variant) is None:
            h = random.choice(list(self.variants.keys()))
            handler = self.variants[h]
        else:
            handler = self.variants[variant]
        return await handler(self, client, message)


class SoundMeme(Meme):

    def __init__(self, cmd, *aliases):
        super(SoundMeme, self).__init__(cmd, *aliases)
        self.type = 'sound'


class TextMeme(Meme):

    def __init__(self, cmd, *aliases):
        super(TextMeme, self).__init__(cmd, *aliases)
        self.type = 'text'


class TTSMeme(Meme):

    def __init__(self, cmd, *aliases):
        super(TTSMeme, self).__init__(cmd, *aliases)
        self.type = 'tts'
