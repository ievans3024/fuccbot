import asyncio
import logging
import random

__author__ = 'ievans3024'

logger = logging.getLogger('discord')


class Bot(object):

    def __init__(self, token, client):
        self.token = token
        self.roles = []
        self.channels = []
        self.memes = {}
        self.client = client
        self.quick_help = 'No meme specified. Try "!fuccbot help" or "!fuccbot help memes".'

    @property
    def __command_map(self):
        """Maps commands to themselves and aliases to their respective commands."""
        _map = {}
        for k, v in self.memes.items():
            _map[k] = k
            for a in v.aliases:
                _map[a] = v.command
        return _map

    @property
    def __general_help(self):
        """General help text."""
        return '''
!fuccbot help

\tAliases: h

\tVariants:

\t\tmemes -- !fuccbot help memes -- lists available memes
\t\t<meme> -- !fuccbot help <meme> -- get more info about a meme
'''

    @property
    def __random_help(self):
        return '''
!fuccbot random

\tAliases: rand

\tVariants: None

\t!fuccbot random -- do a random meme
'''

    @property
    def __meme_list(self):
        """A text list of currently registered memes."""
        text_nodes = ['\nDank Maymays:', '']
        memes = list(self.memes.keys())
        memes.append('random')
        memes = sorted(memes)
        text_nodes += memes
        return '\n\t'.join(text_nodes)

    async def do_meme(self, message, channel):
        command = message.content
        parts = command.split(' ')[1:]
        if len(parts) > 0:
            if parts[0] in {'help', 'h'}:
                # print help text in calling channel
                if len(parts) == 1:
                    help_text = self.__general_help
                else:
                    # print meme help
                    if parts[1] == 'memes':
                        help_text = self.__meme_list
                    elif parts[1] in {'random', 'rand'}:
                        help_text = self.__random_help
                    elif parts[1] in self.__command_map:
                        meme = self.__command_map[parts[1]]
                        help_text = self.memes.get(meme).help
                    else:
                        help_text = self.__general_help
                await self.client.send_message(channel, help_text)
            elif parts[0] in {'random', 'rand'}:
                meme = self.memes[random.choice(list(self.memes.keys()))]
            elif parts[0] in self.__command_map:
                meme = self.memes.get(self.__command_map[parts[0]])
                if len(meme.variants) > 1:
                    if len(parts) > 1:
                        if parts[1] in meme.variants:
                            v = parts[1]
                        elif parts[1] in meme.variant_aliases:
                            v = meme.variant_aliases[parts[1]]
                        else:
                            v = None
                        if v is not None:
                            return await meme.do(self.client, message, variant=v)
                        else:
                            msg = 'Try again, meat popsicle:\n'
                            help_text = meme.help
                            return await self.client.send_message(channel, msg + help_text)
                return await meme.do(self.client, message)
            else:
                msg = 'Try again, meat popsicle:\n'
                help_text = self.__general_help
                return await self.client.send_message(channel, msg + help_text)
        else:
            return await self.client.send_message(channel, self.__general_help)

    def register_meme(self, meme):

        # compile a list of current commands and aliases
        current_commands = ['help', 'h', 'random', 'rand']
        added_aliases = []
        skipped_aliases = []
        for k, v in self.memes.items():
            current_commands.append(k)
            current_commands += (v.aliases or [])
        if len(meme.aliases):
            added_aliases = [a for a in meme.aliases if a not in current_commands]
            skipped_aliases = [a for a in meme.aliases if a not in added_aliases]
        if meme.command in current_commands:
            logger.warn('Meme command {command} already exists, skipping.'.format(command=meme.get('command')))
        else:
            meme.aliases = added_aliases
            if len(skipped_aliases):
                logger.warn(
                    'Meme aliases skipped, already exist in other memes as commands or aliases: {0}'.format(
                        skipped_aliases
                    )
                )
            self.memes[meme.command] = meme

    def register_memes(self, *memes):
        for m in memes:
            self.register_meme(m)

