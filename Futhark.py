import discord
from discord.ext import commands
import random
import sys, traceback
import pickle

"""These examples make use of Python 3.6.2 and the rewrite version on the lib.
    
    For examples on cogs for the async version:
    https://gist.github.com/leovoel/46cd89ed6a8f41fd09c5
    
    Rewrite Documentation:
    http://discordpy.readthedocs.io/en/rewrite/api.html
    
    Rewrite Commands Documentation:
    http://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html
    
    Familiarising yourself with the documentation will greatly help you in creating your bot and using cogs.
    """

def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""
    
    # Can use spaces. Keep simple though.
    prefixes = ['f!']
    
    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow this prefix to be used in DMs
        return ['f!']
    
    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = ['cogs.devs',
                      'cogs.god',
                      'cogs.registering',
                      'cogs.travel',
                      'cogs.survival']

bot = commands.Bot(command_prefix=get_prefix, description="The official Project Futhark bot", self_bot=False)
bot.remove_command('help')

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""
    
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: v1.0.0\n')
    
    await bot.change_presence(activity=discord.Activity(name="GOD",
                                                        type=0),status=discord.Status.online)
    print(f'Successfully logged in and booted...!\n')

bot.run('TOKEN', bot=True, reconnect=True)
