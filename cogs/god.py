import discord
from discord.ext import commands
import pickle
import time
import random

class SayCog:

    def __init__(self,bot):
        self.bot = bot

    @commands.group(name='god',aliases=['g'])
    async def GOD(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("No subcomand sent.")

    #Allows the bot to seem like it's 'saying' stuff.
    @GOD.command(name='say')
    @commands.has_any_role('GOD') #Means that only Ichors and GODs can run the command.
    async def SayMessage(self, ctx, channel:discord.TextChannel, *, message:str):
        await channel.send(message)
        await ctx.message.delete() #Delete the message that invoked the command

    #Updates the presence. See FAQ of docs under "How do I set the 'Playing' status?" for more info
    @GOD.command(name='presence')
    @commands.has_any_role('GOD')
    async def ChangingPresence(self,ctx,activityType,*,activityName):
        await ctx.message.delete()
        await self.bot.change_presence(activity=discord.Activity(name=activityName,
                                                        type=activityType))

    #Modifies the status dot of the bot for 4 different settings.
    @GOD.command(name='status')
    @commands.has_any_role('GOD')
    async def ChangingStatus(self,ctx,status):
        await ctx.message.delete()
        if status == '1':
            await self.bot.change_presence(status=discord.Status.online)
        elif status == '2':
            await self.bot.change_presence(status=discord.Status.idle)
        elif status == '3':
            await self.bot.change_presence(status=discord.Status.dnd)
        elif status == '4':
            await self.bot.change_presence(status=discord.Status.invisible)
        else:
            await ctx.send(content="Invalid integer.",delete_after=5)

    @GOD.command(name='smite')
    @commands.has_any_role('GOD')
    async def Smite(self, ctx, member: discord.Member= None, strength: float = 0, maxStrength:float = 0.05, strikeProbability :float=100):
        await ctx.message.delete()
        if maxStrength == 0.05:
            maxStrength=strength
        #Checks that they have selected a memeber.
        if member is None:
            await ctx.send("Please select someone to smite.")
            return
        #Get the player data
        playerData = pickle.load(open('players.data','rb'))
        #Checks if the strike will hit.
        strikeChance = random.randint(0,100)
        if strikeChance <= strikeProbability:
            #Checks if strength will be random (input of 0)
            if strength == 0:
                if maxStrength == 0:
                    await ctx.send(content="If you are going to use a random, please set a max strength.",delete_after=3)
                    return
                #Sets new strength
                strength = random.randint(0,maxStrength)
            #Deals the damage equal to the strength
            playerData[f'{member.id}']['status']['health'] -= strength
            #Informs the user that they were smited.
            await ctx.send(f"{member.mention} was smited for {strength} hit points by {ctx.author.mention}.")
            if playerData[f'{member.id}']['status']['health'] <= 0 :
                await member.send("You have died. Contact an Ichor to be revived. The timer is not currently working. If possible, contact the Ichor that killed you.")
                #Kills the player and sets up for the timers.
                playerData[f'{member.id}']['isDead'] = True
                playerData[f'{member.id}']['deadAmount'] += 1
                playerData[f'{member.id}']['deathTime'] = time.time()
            pickle.dump(playerData,open('players.data','wb'))
        else:
            await ctx.send(f"Lightning striked close to {member.mention} but misses...")

    @GOD.command(name='revive')
    @commands.has_any_role('GOD')
    async def Revive(self,ctx,member: discord.Member = None):
        playerData = pickle.load(open('players.data','rb'))
        if member is None:
            await ctx.send("Please select a member.")
            return
        playerData[f'{member.id}']['isDead'] = False
        await ctx.send(f"{member.display_name} was revived by {ctx.author.display_name}")
        pickle.dump(playerData,open('players.data','wb'))

def setup(bot):
    bot.add_cog(SayCog(bot))
