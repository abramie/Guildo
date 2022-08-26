# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 12:56:35 2022

@author: jerem

launch with python command (from anaconda prompt), spyder deconne avec discord.py
database need date, faut gerer des sous thread pour chaque semaine, enregistrer l'id du message pour chaque nouvelle table
Inscription a la table via reaction, gerer le maximum d'inscription pour une table donner
gerer update name discord des inscrit/meneur
"""

# bot.py
import os

import discord
import random
from dotenv import load_dotenv
#import nest_asyncio
#nest_asyncio.apply()
from discord.ext import commands,tasks
import sqlite3
from datetime import time
intents = discord.Intents.all()
#import asyncpg
dt = time(hour=16,minute=47)
db_file = os.path.dirname(__file__) + '/table.db'
def create_database():
    print("creation of the database ")
    con = sqlite3.connect(db_file)
    
    cur = con.cursor()
    
    # Create table
    cur.execute('''CREATE TABLE tables
                   (nom text, MJ_name text, MJ_id real, msg_ID real)''')
    
    # Insert a row of data
    cur.execute("INSERT INTO tables VALUES ('dnd','abramie',2, 12)")
    
    # Save (commit) the changes
    con.commit()


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='G!',intents=intents)

if not os.path.isfile(db_file): 
    create_database()
con = sqlite3.connect(db_file)
   
cur = con.cursor()
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.

@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )
    #sendTableStatus.add_exception_type(asyncpg.PostgresConnectionError)
    sendTableStatus.start()
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Salut {member.name}, Bienvenue sur le serveur!'
    )


@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    
    response = random.choice(brooklyn_99_quotes)
    await ctx.channel.send("hey " + ctx.author.mention + " " +response)
@bot.command(name='open-table')
@commands.has_role('Guildien')
async def open_table(ctx):
    if ctx.channel.name == "test_bot":
        cur.execute("select * from tables")
        print(cur.fetchall())
        await ctx.channel.send("nouvelle table créer  " + ctx.author.mention)
    else:
        await ctx.channel.send("Mauvais salon ! " + ctx.author.mention)

@bot.command()
async def test(ctx, *, arg):
    await ctx.send(arg)
        
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    else:
    	await ctx.send('erreur avec la commande')
def check_if_it_is_me(ctx):
    return ctx.message.author.id == 210147166583259136

@bot.command(name='id', help='print the id of the channel')
@commands.check(check_if_it_is_me)
async def getId(ctx):
    
    print(f'channel id : {ctx.channel.id}\n' 
          f'user id : {ctx.author.id}')
    channel = bot.get_channel(967770476900413460)
    await channel.send("test message id")
@tasks.loop(seconds=3.0,count=5)
async def sendTableStatus():
    print("loop valid")
    channel = bot.get_channel(967770476900413460)
    await channel.send("test message")
bot.run(TOKEN)
con.close()
