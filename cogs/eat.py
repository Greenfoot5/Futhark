from discord.ext import commands
import discord
import pickle

class EatCog:
    
    def __init__(self, bot):
        self.bot = bot
        self.Consumables = ['raspberry']

#Implement embed inventory choice like in cah.

@commands.command(name='eat')
async def Eating(self,ctx):
    playerData = pickle.load(open('player.data','rb'))
    if consumable == None:
        for i in range(0,len(playerData[f'{ctx,author.id}']['inventory'])):
            if playerData[f'{ctx.author.id}']['inventory'][f'{i}']['name'] in self.Consumables:
                consumable = playerData[f'{ctx.author.id}']['inventory'][f'{i}']
    playerData[f'{ctx.author.id}']['status']['thirst'] = 0
    playerData[f'{ctx.author.id}']['status']['hunger'] = 0
    pickle.dump(playerData,open('player.data','wb'))
    await ctx.send("You hunger and thirst have been sated.")

def setup(bot):
    bot.add_cog(EatCog(bot))

