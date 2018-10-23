from discord.ext import commands
import discord
import pickle
        
class TravelCog:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='travel', aliases=['t'])
    async def Traveling(self, ctx):
        if ctx.invoked_subcommand is None:
            playerData = pickle.load(open('players.data','rb'))
            if playerData[f'{ctx.author.id}']['currentLocation'] == 'stones':
                embed=discord.Embed(name='Travel locations',
                                    description='Below are the locations you can travel to',
                                    colour=0x00FF88)
                embed.set_author(name=ctx.author.display_name,
                                 icon_url=ctx.author.avatar_url_as(format='png'))

                embed.add_field(name='Valid locations',
                                value='#temple')
                embed.add_field(name='Restricted areas',
                                value='#empty-lot\n#outskirts')

                embed.set_footer(text=self.bot.get_guild(476728702131109888).name,
                                 icon_url=self.bot.get_guild(476728702131109888).icon_url_as(format='png'))

                await ctx.send(content='',embed=embed)
            elif playerData[f'{ctx.author.id}']['currentLocation'] == 'temple':
                embed=discord.Embed(name='Travel locations',
                                    description='Below are the locations you can travel to',
                                    colour=0x00FF88)
                embed.set_author(name=ctx.author.display_name,
                                 icon_url=ctx.author.avatar_url_as(format='png'))

                embed.add_field(name='Valid locations',
                                value='#stones')

                embed.set_footer(text=self.bot.get_guild(476728702131109888).name,
                                 icon_url=self.bot.get_guild(476728702131109888).icon_url_as(format='png'))

                await ctx.send(content='',embed=embed)
            else:
                await ctx.send("You have hit the dead end of no return...")

    @Traveling.command(name='stones')
    async def TravelingToStones(self,ctx):
        playerData = pickle.load(open('players.data','rb'))
        if playerData[f'{ctx.author.id}']['currentLocation'] == 'stones':
            await ctx.send("You are already there silly!")
        elif playerData[f'{ctx.author.id}']['currentLocation'] in ['temple','empty-lot','outskirts']:
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
            playerData[f'{ctx.author.id}']['currentLocation'] = 'stones'
            await ctx.author.send("You have travelled to `#stones`. How you had a nice journey.")
            pickle.dump(playerData,open('players.data','wb'))

    @Traveling.command(name='temple')
    async def TravelingToTemple(self,ctx):
        playerData = pickle.load(open('players.data','rb'))
        if playerData[f'{ctx.author.id}']['currentLocation'] == 'temple':
            await ctx.send("You are already there silly!")
        elif playerData[f'{ctx.author.id}']['currentLocation'] in ['stones']:
            #Sets up the permissions in each of the channel
            #stones text channel
            await self.bot.get_channel(481588206836645888).set_permissions(ctx.message.author,read_messages=True,send_messages=False,read_message_history=False)
            #temple text channel
            await self.bot.get_channel(481588227086745611).set_permissions(ctx.message.author,read_messages=True,send_messages=True,read_message_history=True)
            #chatting voice channel
            await self.bot.get_channel(481588260351639555).set_permissions(ctx.message.author,overwrite=None)
            #empty-lot text channel
            await self.bot.get_channel(481588293591629835).set_permissions(ctx.message.author,overwrite=None)
            #outskirts text channel
            await self.bot.get_channel(481588354157379604).set_permissions(ctx.message.author,overwrite=None)
            playerData[f'{ctx.author.id}']['currentLocation'] = 'temple'
            pickle.dump(playerData,open('players.data','wb'))
            await ctx.author.send("You have travelled to `#temple`. How you had a nice journey.")

    @Traveling.command(name='outskirts')
    async def TravelingToOutskirts(self,ctx):
        playerData = pickle.load(open('players.data','rb'))
        if playerData[f'{ctx.author.id}']['currentLocation'] == 'outskirts':
            await ctx.send("You are already there silly!")
        elif playerData[f'{ctx.author.id}']['currentLocation'] in ['stones']:
            await ctx.send("Oooo... wouldn't go there... looks kinda scary...")

    @Traveling.command(name='empty-lot')
    async def TravelingToEmptyLot(self,ctx):
        playerData = pickle.load(open('players.data','rb'))
        if playerData[f'{ctx.author.id}']['currentLocation'] == 'empty-lot':
            await ctx.send("You are already there silly!")
        elif playerData[f'{ctx.author.id}']['currentLocation'] in ['stones']:
            await ctx.send("You can't get to the field with all that barbed wire around it!")

            
def setup(bot):
    bot.add_cog(TravelCog(bot))
