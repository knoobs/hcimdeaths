# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 23:37:59 2021

@author: kneub
"""

import nest_asyncio
nest_asyncio.apply()

import discord
from discord.ext import commands, tasks
import scraper as sc
from config import Channels, Constants, APIs

TOKEN = APIs.DISCORD_KEY

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.send("Hey there bucko... you don't have permission for that!")

@bot.command(name='tweet')
async def force_tweet(ctx, *argv):

    # Check channel
    bot_channel = Channels.BOT_CHANNELS
    approved_channel = discord.utils.get(ctx.guild.channels, name=bot_channel)
    message_channel = ctx.message.channel
    if str(message_channel) in Channels.BLACKLIST_CHANNELS:
        print("Command received in unapproved channel")
        await approved_channel.send(f"{ctx.author.mention} Please use this channel for the bot.")

    name = ' '.join(argv)
    print(f"Getting image for {name}")
    stats = sc.get_player_stats(name)
    sc.create_image(name, stats)
    text = sc.create_text(name, stats)
    await approved_channel.send(text)
    await approved_channel.send(file=discord.File(f"tweet_images/{name.lower().replace(' ', '_')}.png"))

@tasks.loop(minutes=30)
async def my_background_task():
    # Get channels to interact with
    general = bot.get_channel(Channels.GENERAL)
    bot_channel = bot.get_channel(Channels.BOT_CHANNEL)

    # Check for new deaths
    await bot_channel.send(f"Checking top {str(Constants.MAX_RANK)} hiscores for new deaths...")
    names = sc.get_dead_names('hcim_deaths.json')
    tweet_names = sc.write_dead_names('hcim_deaths.json', names)
    await bot_channel.send("Done.")

    # Post images
    for name in tweet_names:
        # Get text and image
        stats = sc.get_player_stats(name)
        text = sc.create_text(name, stats)
        image = f"tweet_images/{name.lower().replace(' ', '_')}.PNG"

        # Post tweet on twitter and in discord
        sc.post_tweet(text, image)
        await general.send(text)
        await general.send(file=discord.File(image))

@my_background_task.before_loop
async def my_background_task_before_loop():
    await bot.wait_until_ready()

my_background_task.start()
bot.run(TOKEN)