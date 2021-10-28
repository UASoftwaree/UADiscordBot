import discord
from discord.ext import commands
from discord import Client
from discord.utils import get

#Host Package
import asyncio
from keep_alive import keep_alive
import os
import json

#Python Functions
import datetime

#Bot Config#
Prefix="rs!"
bot = commands.Bot(command_prefix=Prefix)
bot.remove_command('help')

@bot.event
async def on_message(message):
  for file in message.attachments:
    if file.filename.endswith(('.exe', '.dll', '.msi')):
      await message.delete()
      await message.author.send(f'Your file may contain some form on hacks, cheats or virus. We donot allow this in {message.guild.name}')

#Bot Deletes Server Invites
@bot.event
async def on_message(message):
  if message.content.startswith('https://discord.gg'):
    await message.delete()
    await message.author.send(f'We do not allow discord invites in {message.guild.name}')

#Bot Login#
keep_alive()
token = os.environ['Token']
bot.run(token)