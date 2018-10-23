import discord
from discord.ext import commands

class SayCog:

    def __init__(self,bot):
        self.bot = bot

    #Allows the bot to seem like it's 'saying' stuff.
    @commands.has_any_role('Ichor','GOD') #Means that only Ichors and GODs can run the command.
    @commands.command(name='say')
    async def SayMessage(self, ctx, channel:discord.TextChannel, *, message:str):
        await channel.send(message)
        await ctx.message.delete()

    #Updates the presence. See FAQ of docs under "How do I set the 'Playing' status?" for more info
    @commands.has_any_role('Ichor','GOD')
    @commands.command(name='presence')
    async def ChangingPresence(self,ctx,activityType,*,activityName):
        await self.bot.change_presence(activity=discord.Activity(name=activityName,
                                                        type=activityType))

    #Modifies the status dot of the bot for 4 different settings.
    @commands.has_any_role('Ichor','GOD')
    @commands.command(name='status')
    async def ChnagingStatus(self,ctx,status):
        if status == '1':
            await self.bot.change_presence(status=discord.Status.online)
        elif status == '2':
            await self.bot.change_presence(status=discord.Status.idle)
        elif status == '3':
            await self.bot.change_presence(status=discord.Status.dnd)
        elif status == '4':
            await self.bot.change_presence(status=discord.Status.invisible)
        else:
            await ctx.send("Invalid integer.")

def setup(bot):
    bot.add_cog(SayCog(bot))
