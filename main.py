#Discord Packages
import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import Embed
from discord.utils import escape_markdown, escape_mentions
from discord.utils import get

#Roblox
from ro_py import Client

#Host Package
from keep_alive import keep_alive
import json
import requests


#Python Functions
import os
import asyncio
import random
import time
import datetime


#Bot Config

#Change Prefrix
Prefix = "r!"
bot = commands.Bot(command_prefix=Prefix)
roblox = Client(os.environ['RobloxSecurity'])
bot.remove_command('help')

#OS Function
Token = os.environ['Token']

#Bot Activity
@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name="r!help"))
  
#######################################
#     Help Commands
#Changing the help command#
@bot.command()
async def help(ctx):
    em = discord.Embed(
      title="",
      description="__**[RoNetwork](https://daulric.repl.co)**__ by **[@daulric](https://twiiter.com/daulric)**",
      color=discord.Color.red())
    
    em.set_thumbnail(url=ctx.guild.icon_url)
    em.add_field(name="__**Moderation**__", value="```r!helpmod```")
    em.add_field(name="Channel", value="```r!helpchannel```")
    em.add_field(name="__**Fun**__", value="```r!helpfun```")
    em.add_field(name="__**Roles**__", value="```r!helproles```")
    em.add_field(name="__**Roblox**__", value="```r!helproblox```")
    em.add_field(name="__**Bot Information**__", value="```r!helpbotinfo```")
    em.add_field(name="Settings", value="```r!helpsettings```")
    
    await ctx.send(embed=em)

#Help Moderation
@bot.command()
async def helpmod(ctx):
    em = discord.Embed(
      title = "",
      description = "",
      color=discord.Color.red()
    )
    em.add_field(name="**Mod Commands**", value="```mute``` ```unmute``` ```kick``` ```changedisplay```")

    await ctx.send(embed=em)

#Help Channel
@bot.command()
async def helpchannel(ctx):
    em = discord.Embed(
      title = "",
      description = "",
      color=discord.Color.red()
    )
    em.add_field(name="**Channel Commands**", value="```createchannel``` ```deletechannel``` ```slowmode``` ```clear``` ```lock``` ```unlock```")

    await ctx.send(embed=em)

#Help Fun
@bot.command()
async def helpfun(ctx):
    em = discord.Embed(
      title = "",
      description = "",
      color=discord.Color.red()
    )
    em.add_field(name="**Fun**", value="```getpfp``` ```dm``` ```say``` ```tts``` ```whois``` ```jokes``` ```think``` ```rateme``` ```bodyscan``` ```thought``` ```hack``` ```hackdiscord``` ```meme```")

    await ctx.send(embed=em)

#Help Roles
@bot.command()
async def helproles(ctx):
    em = discord.Embed(
      title = "",
      description = "",
      color=discord.Color.red()
    )
    em.add_field(name="**Roles**", value="```createrole``` ```removerole``` ```giverole```")

    await ctx.send(embed=em)

#Help Roblox
@bot.command()
async def helproblox(ctx):
    em = discord.Embed(
      title = "",
      description = "",
      color=discord.Color.red()
    )
    em.add_field(name="**Roblox**", value="```rbxuser```")

    await ctx.send(embed=em)

#Bot Info
@bot.command()
async def helpbotinfo(ctx):
    em = discord.Embed(
      title = "",
      description = "",
      color=discord.Color.red()
    )
    em.add_field(name="**Bot Information**", value="```status``` ```whoareyou``` ```botinfo``` ```invite``` ```joinbeta``` ```bots```")

    await ctx.send(embed=em)

#Help Settings
@bot.command()
async def helpsettings(ctx):
    em = discord.Embed(
      title = "",
      description = "",
      color=discord.Color.red()
    )
    em.add_field(name="**Settings**", value="```toggle```")

    await ctx.send(embed=em)

#################################
#      Help Section Above
################################

#Enable/Disable Command
@bot.command()
@commands.has_permissions(manage_messages=True)
async def toggle(ctx, *, command):
  command = bot.get_command(command)

  if command is None:
    await ctx.send("I can't find a command with that name!")

  elif ctx.command == command:
    await ctx.send("You cannot disable this command.")

  else:
    command.enabled = not command.enabled
    ternary = "enabled" if command.enabled else "disabled"
    await ctx.send(f"I have {ternary} {command.qualified_name} for you!")


#########################################################
#       Owner-Only Commands
#########################################################

#Owner Help Command
@bot.command()
@commands.is_owner()
async def blacklist(ctx):
  
  embed = discord.Embed(title="", description="[We are One](https://daulric.repl.co)", color = discord.Color.purple())

  embed.add_field(name="Blacklist Commands", value="`broadcast`, `template`", inline=False)

  await ctx.send(embed=embed)


#Server-Wide Broadcast
@bot.command(pass_context=True)
@commands.is_owner()
async def broadcast(ctx, *, msg):
  for server in bot.guilds:
    for channel in server.text_channels:
      try:
        await channel.send(msg)
      except Exception:
        continue
      else:
        break

#Server Template
@bot.command()
@commands.is_owner()
async def template(ctx, name):
  await ctx.guild.create_template(name = name, description = None)
  await ctx.send('Done.')

#Server Ban


###############
# Ping Request
###############
@bot.command(aliases=["ms"])
async def ping(ctx):

  embed = discord.Embed(
    title="Ping Request",
    description=f'My ping is {bot.latency}!'
  )
  await ctx.send(embed=embed)

##########################################################
#               MODERATRION        COMMANDS
##########################################################

#Mute command
@bot.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="Muted", description=f"{member.mention} was muted ", colour=discord.Color.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" you have been muted from: {guild.name} reason: {reason}")

#Ummute Command
@bot.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   await member.send(f" you have unmuted from: - {ctx.guild.name}")
   embed = discord.Embed(title="Unmute", description=f" unmuted-{member.mention}",colour=discord.Colour.light_gray())
   await ctx.send(embed=embed)

#Kick Command
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason==None:
      reason=" no reason provided"
    await ctx.guild.kick(member)
    await ctx.send(f'User {member.mention} has been kicked for {reason}')

#Changing Display Name
@bot.command(pass_context=True)
async def changedisplay(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')

##########################################################
#                     STATUS AREA
##########################################################

#Bot Status Event#
@bot.command(status = "Prints details of Server")
async def status(ctx):
    owner=str(ctx.guild.owner)
    region = str(ctx.guild.region)
    guild_id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    desc=ctx.guild.description
    
    embed = discord.Embed(
        title=ctx.guild.name + " Server Information",
        description=desc,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=guild_id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)

    members=[]
    async for member in ctx.guild.fetch_members(limit=150) :
        await ctx.send('Name : {}\t Status : {}\n Joined at {}'.format(member.display_name,str(member.status),str(member.joined_at)))

#Who are You
@bot.command()
async def whoareyou(ctx):
    text = ("**I am RoNetBot and I was created by daulric :)**")
    await ctx.send(text)

#Bot info
@bot.command()
async def botinfo(ctx):
  em = discord.Embed(
    title='__**Bot Info**__',
    description=''
  )

  em.add_field(name="Programing Language", value="Python", inline=False)
  em.add_field(name="Software", value="[Repl.it](https://repl.it)", inline=False)
  em.add_field(name="Owner", value="[@Usered](https://twitter.com/UseredDev)", inline=False)

  em.set_footer(text="I am a more advance machine than my Brother @RoNetBot")

  await ctx.send(embed=em)

#UserInfo
@bot.command()
async def whois(ctx, user: discord.Member=None):

    embed = discord.Embed(colour=user.color,timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Info - {user}"),
    embed.set_thumbnail(url=user.avatar_url),
    embed.set_footer(text=f'Requested by - {ctx.author}',
  icon_url=ctx.author.avatar_url)

    embed.add_field(name='ID:',value=user.id,inline=False)
    embed.add_field(name='Name:',value=user.display_name,inline=False)

    embed.add_field(name='Created at:',value=user.created_at,inline=False)
    embed.add_field(name='Joined at:',value=user.joined_at,inline=False)

    embed.add_field(name='Bot?',value=user.bot,inline=False)
    embed.add_field(name='Top Role:',value=user.top_role.mention,inline=False)

    await ctx.send(embed=embed)

#Join the beta
@bot.command()
async def joinbeta(ctx):

  embed = discord.Embed(
    title='',
    description=''
  )

  embed.add_field(name='____', value='**[Beta Testing Server](https://discord.gg/sK967BfmhU)**', inline=True)

  embed.set_footer(text='@Usered')
  
  await ctx.send(embed=embed)

#More Bots You Can User
@bot.command()
async def bots(ctx):

  embed = discord.Embed(
    title='',
    description='More Bots by **[@daulric](https://twitter.com/daulric)**',
    color=discord.Color.red())

  embed.add_field(name="Security", value="**[RSecurity](https://discord.com/api/oauth2/authorize?client_id=895079951978627102&permissions=8&scope=bot)**", inline=True)
  embed.add_field(name="Canary Man", value="**[RoNetwork Canary](https://discord.com/api/oauth2/authorize?client_id=881919783782744064&permissions=8&scope=bot)**", inline=False)

  await ctx.reply(embed=embed)


##########################################################
#            ROLES AREA
##########################################################

#Create Roles
@bot.command(brief=' - This wil create a role on the server',aliases=['make_role'])
@commands.has_permissions(manage_roles=True) # Check if the user executing the command can manage roles
async def createrole(ctx, *, name):
	guild = ctx.guild
	await guild.create_role(name=name)
	await ctx.send(f'Role `{name}` has been created')

#Give Role
@bot.command(pass_context=True)
async def giverole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"**hey {user.name} has been giving a role called {role.name}**")

#Remove Role
@bot.command(pass_context=True)
async def removerole(ctx, user: discord.Member, role: discord.Role):
  await user.remove_roles(role)
  await ctx.send(f"**{user.name} got his {role.name} removed form his profile!!**")


##########################################################
#                  FUN    AREA
##########################################################

#DM User
@bot.command()
async def dm(ctx, user: discord.User, *, message):
  await user.send(message)

#Say Command
@bot.command()
async def say(ctx, message=None):
  await ctx.send(message)

#TTS Voice
@bot.command()
async def tts(ctx, message):
  await ctx.send(message, tts=True)

#User PFP
@bot.command()
async def getpfp(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    em = discord.Embed(title=str(member), color=0xAE0808)
    em.set_image(url=member.avatar_url)
    await ctx.send(embed=em)

#Jokes
@bot.command()
async def jokes(ctx):
  jokes = ["What's long and have seamen ..... a submarine", "Your mama so fat, she jumped from a roof just to break a stick", "I only know 25 letters of the alphabet. I don't know y.", "I don't trust those trees. They seem kind of shady."
, "That car looks nice but the muffler seems exhausted.", ]

  await ctx.send(f"{random.choice(jokes)}")

#Think Twice
@bot.command()
async def think(ctx):
  think = ["Dude if you drop a soap, is the floor clean?, or is the soap dirty?", "If you cut ur leg of, where will you feel the pain?", "Bro, history is gonna get longer as time goes on", "If a fly loses its wings, is it called walk?", "You can't remember what memories you lost?", "If you someone hates you, and you hate them back does that makes you the hater", "Money is only useful when you get rid of it", "Most pets die not knowing their owner's name", "If youre born a billionaire, you got everything in life unlocked already", "Every single odd number has an 'e' in it", "People who wear glasses pay to live in HD", "Why is it called 'taking a dump' when you're leaving it", "If your finger has fingertip, but your toe don't have toetip, yet you can tiptoe but you can't fingertip", "When computers get hot they freeze", "When UFO is identified as a UFO it's no longer a UFO", "Water companies only produce plastic"]

  await ctx.send(f"{random.choice(think)}")

#Rating Users
@bot.command(pass_context=True)
async def rateme(ctx):
  await ctx.send(f"You are {random.randint(1, 100)}% a loser (its just a joke!!)")

#Body Scan (meme)
@bot.command(pass_context=True)
async def bodyscan(ctx):
  await ctx.send(f"You are {random.randint(1, 7)} foot tall")
  time.sleep(1)
  await ctx.send(f"You weighed {random.randint(1, 500)} pounds")
  time.sleep(1)
  await ctx.send(f"You are {random.randint(1, 100)}% free of cholesterol")
  time.sleep(1)
  await ctx.send(f"You have {random.randint(1, 200)} IQ")
  time.sleep(3)
  await ctx.send("Life is tough!! don't worry we will get true it")

#Thought of the day
@bot.command(pass_context=True)
async def thought(ctx):
  thought = ["Never give up on your dreams", "Work hard for what you want", "Don't envy other peoples stuff, work for it"]

  await ctx.send(random.choice(thought))
  time.sleep(86400)

#Hack Meme
@bot.command()
async def hack(ctx, user: discord.User):
  await ctx.send("Hacking User")
  time.sleep(2)
  await ctx.send("Grabbing user's ip addresss")
  time.sleep(2)
  await ctx.send("Sending a DDoS attack")
  time.sleep(2)
  await ctx.send("Getting User's Social Security")
  time.sleep(2)
  await ctx.send("Getting user's password")
  time.sleep(2)
  await ctx.send("Stealing User Token")
  time.sleep(2)
  await ctx.send("Storing Data in the Server")
  time.sleep(2)
  await ctx.send("Awaiting File")
  time.sleep(3)
  await ctx.send("Hack completed")
  await ctx.send(file=discord.File("HackMeme/userhack.txt"))

#Memes
@bot.command()
async def meme(ctx):
  path = random.choice(os.listdir("Memes/"))
  await ctx.send(file=discord.File("Memes/"+path))

#Dicord Hack Meme
@bot.command()
async def hackdiscord(ctx):
  await ctx.send("Discord Hack Started")
  time.sleep(2)
  await ctx.send("Attacking Servers")
  time.sleep(2)
  await ctx.send("Stealing Users Information")
  time.sleep(2)
  await ctx.send("Stealing all IP Addresses")
  time.sleep(2)
  await ctx.send("Gathering All Information")
  time.sleep(1)
  await ctx.send("........")
  time.sleep(2)
  await ctx.send("Hack Completed!!")
  await ctx.send(file=discord.File("HackMeme/discordhack.txt"))


##############################################
#        Channels
##############################################
#Create Channel
@bot.command(aliases=['createch'])
async def createchannel(ctx, channelName):
  guild = ctx.guild

  embed = discord.Embed(
    title = 'New Channel has been Created',
    description = '{}has been created.'.format(channelName)
  )
  if ctx.author.guild_permissions.manage_channels:
    await guild.create_text_channel(name='{}'.format(channelName))
    await ctx.send(embed=embed)


#Delete Channel
@bot.command(aliases=['delch'])
async def deletechannel(ctx, channel: discord.TextChannel):
  embed = discord.Embed(
    title = "Success",
    description = f"Channel: {channel} has been deleted."
  )
  if ctx.author.guild_permissions.manage_channels:
    await ctx.send(embed=embed)
    await channel.delete()

#Clear Chat
@bot.command(aliases= ['purge','delete'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
   if amount == None:
       await ctx.channel.purge(limit=100)
   else:
       await ctx.channel.purge(limit=100)
       await ctx.send("Messages has been deleted")

#Chat Lock/Unlock
@bot.command()
@commands.has_permissions(manage_channels = True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send( ctx.channel.mention + " ***is now in lockdown.***")
#unlock
@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + " ***has been unlocked.***")

#Slowmode
@bot.command(aliases=['slm'])
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")

#######################################
#    Roblox 
#######################################
#Who Is Roblox User
@bot.command()
async def rbxuser(ctx, username):
    user = await roblox.get_user_by_username(username)
    embed = Embed(title=f"Info for {user.name}")
    embed.add_field(
        name="Username",
        value="`" + user.name + "`"
    )
    embed.add_field(
        name="Display Name",
        value="`" + user.display_name + "`"
    )
    embed.add_field(
        name="User ID",
        value="`" + str(user.id) + "`"
    )
    embed.add_field(
        name="Description",
        value="```" + (escape_markdown(user.description or "No description")) + "```"
    )
    await ctx.send(embed=embed)

#Ranking Users in a Group#
#Promote Users
@bot.command()
@commands.has_permissions(manage_guild=True)  # Guild managers only.
async def promote(ctx, username):
  group = await roblox.get_group(7819173)  # Group ID here
  member = await group.get_member_by_username(username)
  await member.promote()
  await ctx.send("Promoted user.")

#Demote Users
@bot.command()
@commands.has_permissions(manage_guild=True)  # Guild managers only.
async def demote(ctx, username):
  group = await roblox.get_group(7819173)  # Group ID here
  member = await group.get_member_by_username(username)
  await member.demote()
  await ctx.send("Promoted user.")

#Set Rank
@bot.command()
@commands.has_permissions(manage_guild=True)  # Guild managers only.
async def setrank(ctx, username, rank: int):
  if 255 >= rank >= 1:  # Make sure rank is in allowed range
    group = await roblox.get_group()  # Group ID here
    member = await group.get_member_by_username(username)
    await member.setrole(rank)  # Sets the rank
    await ctx.send("Promoted user.")
  else:
    await ctx.send("Rank must be at least 1 and at most 255.")

#Shout Message to Roblox Group
@bot.command()
@commands.has_permissions(manage_guild=True)  # Guild managers only.
async def shout(ctx, *, shout_text):
  group = await roblox.get_group(7819173)  # Group ID here
  await group.shout(shout_text)
  await ctx.send("Sent shout.")



#Bot Login
keep_alive()
bot.run(Token)