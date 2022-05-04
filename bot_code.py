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
from discord.ext import commands
import sqlite3

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

client = discord.Client()
bot = commands.Bot(command_prefix='G!')

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
        
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
        
        
bot.run(TOKEN)
con.close()