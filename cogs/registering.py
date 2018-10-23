import discord
from discord.ext import commands
import pickle
import random
import time


"""A simple cog example with simple commands. Showcased here are some check decorators, and the use of events in cogs.

For a list of inbuilt checks:
http://dischttp://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#checksordpy.readthedocs.io/en/rewrite/ext/commands/api.html#checks

You could also create your own custom checks. Check out:
https://github.com/Rapptz/discord.py/blob/master/discord/ext/commands/core.py#L689

For a list of events:
http://discordpy.readthedocs.io/en/rewrite/api.html#event-reference
http://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#event-reference
"""

class Registering:

    def __init__(self, bot):
        self.bot = bot

    #Join message and info to be sent to the user.
    async def on_member_join(self,member):
        welcomeChannel = self.bot.get_channel(481569531194769418)
        await welcomeChannel.send(f"New traveller approaches the gates. It's {member.mention}!")
        embed = discord.Embed(title='Welcome!',
                              description="Welcome traveller to the wonderful world of Futhark!",
                              colour=0x660099)
        embed.set_author(name='Jolly Fellow',
                         icon_url='')
        #embed.set_thumbnail(url=ctx.author.avatar_url_as(format='png'))

        embed.add_field(name='Who are you?',value="I am the Gatekeeper. I make sure that only the right Travellers get into Futhark and make sure they get setup correctly. If they have been before, I welcome them back but avoid all the intro stuff.")
        embed.add_field(name='What is Futhark?',value="I believe you have a game called `The Sims` in your world, correct? It's similar to that but you are the 'sim' and you can do what you want. Now, as it is an early form of civilisation, there isn't much but you can always ask the gods for anything in a temple. Though they may nor act, they will always ready your messages.")
        embed.add_field(name="Why can't I enter?",value="The Gods have deemed the world not  ready. When the time comes simply ask in #gate and you should be permitted!")
        
        embed.set_footer(text=self.bot.get_guild(476728702131109888).name,
                         icon_url=self.bot.get_guild(476728702131109888).icon_url_as(format='png'))
        await member.send(content='',embed=embed)

    @commands.command(name='register')
    async def MemberRegister(self,ctx):
        embed = discord.Embed(title='Register!?',
                              description="I have told you already! The Gods have deemed the world not ready. When the time comes simply ask in #gate and you should be permitted! Now, please don't pseter me! I like my peace and quiet. I don't get much when the gates open.",
                              colour=0x666666)
        embed.set_author(name='Gate Keeper',
                         icon_url='')
        #embed.set_thumbnail(url=ctx.author.avatar_url_as(format='png'))

        embed.add_field(name='When will they open?',value='You will know when it is ready.')
        
        embed.set_footer(text=self.bot.get_guild(476728702131109888).name,
                         icon_url=self.bot.get_guild(476728702131109888).icon_url_as(format='png'))
        await ctx.send(content='',embed=embed)
        playerData = pickle.load(open('players.data','rb'))
        print(playerData)

    @commands.command(name='alpha')
    @commands.has_any_role('Alpha')
    async def MemberAlpha(self,ctx):
        #Adds the Alpha role
        #await ctx.author.add_roles(discord.utils.find(lambda r: r.id == 481834731575443456, ctx.guild.roles))
        embed = discord.Embed(title='Alpha closed.',
                              description="The alpha is now closed. If you want to join early, please wait for the beta.",
                              colour=0x666666)
        embed.set_author(name='Gate Keeper',
                         icon_url='')
        embed.set_thumbnail(url=ctx.author.avatar_url_as(format='png'))

        embed.add_field(name='When will it start?',value="Once it is more stable and there are more features.")
        
        embed.set_footer(text=self.bot.get_guild(476728702131109888).name,
                         icon_url=self.bot.get_guild(476728702131109888).icon_url_as(format='png'))

        #await ctx.send(content='',embed=embed)

        #Get the player data
        playerData = pickle.load(open('players.data','rb'))
        #Checks if the player is dead
        try:
            if playerData[f'{ctx.author.id}']['isDead'] == True:
                await ctx.send("You are dead and cannot join. Please request revival from an Ichor.")
                return
            else:
                playerData[f'{ctx.author.id}'] = {'inventory': [], 'balance': 0, 'team': None, 'currentLocation': 'stones', 'status': {'health': 100, 'hunger': 100, 'thirst': 100}, 'carryLimit': 2, 'carryAmount': 0, 'isIdle': False}
        except KeyError:
            playerData[f'{ctx.author.id}'] = {'inventory': [], 'balance': 0, 'team': None, 'currentLocation': 'stones', 'isDead': False, 'deadAmount': 0, 'status': {'health': 100, 'hunger': 100, 'thirst': 100}, 'carryLimit': 2, 'carryAmount': 0, 'isIdle': False}
        pickle.dump(playerData,open('players.data','wb'))
        
        #Sets up the permissions in each of the channel
        #stones text channel
        await self.bot.get_channel(481588206836645888).set_permissions(ctx.message.author,read_messages=True,send_messages=True,read_message_history=True)
        #temple text channel
        await self.bot.get_channel(481588227086745611).set_permissions(ctx.message.author,read_messages=True,send_messages=False,read_message_history=False)
        #chatting voice channel
        await self.bot.get_channel(481588260351639555).set_permissions(ctx.message.author,connect=True,speak=True,use_voice_activation=True)
        #empty-lot text channel
        await self.bot.get_channel(481588293591629835).set_permissions(ctx.message.author,read_messages=True,send_messages=False,read_message_history=False)
        #outskirts text channel
        await self.bot.get_channel(481588354157379604).set_permissions(ctx.message.author,read_messages=True,send_messages=False,read_message_history=False)
        await ctx.send(content='Welcome back.')
        
def setup(bot):
    bot.add_cog(Registering(bot))
