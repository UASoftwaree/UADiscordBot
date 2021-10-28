import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
import asyncio
import time

bot = commands.Bot(command_prefix="sudo install ")
#Place your Bot Token in Secrets
token = os.environ['Token']
bot.remove_command('help')

@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="sudo install"))

#help
@bot.command()
async def help(ctx):

  em = discord.Embed(
    title="",
    description="__**[Sudo](https://daulric.repl.co)**__ by **[@daulric](https://twiiter.com/daulric)**",
    color=discord.Color.red())
  
  em.add_field(name="__**Some Packages**__", value="`simplypy`", inline=False)

  #footer
  em.set_footer(text='Some of the packages requires you to install node or python. If youre using repl.it, then it will install for you | @daulric')
  
  await ctx.reply(embed=em)


@bot.command()
async def simplepybot(ctx):
  await ctx.send("Sending in..")
  time.sleep(3)
  await ctx.send("3")
  time.sleep(1)
  await ctx.send("2")
  time.sleep(1)
  await ctx.send("1")
  time.sleep(2)
  await ctx.send("Almost ready")
  time.sleep(2)
  await ctx.send(file=discord.File("Packages/SimpleBotPackage.zip"))

keep_alive()
bot.run(token)