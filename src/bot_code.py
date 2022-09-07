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
from discord import app_commands
import sqlite3
from datetime import time as time_dt
import time
import json
import requests
api_url = "http://test.monbacasable.fr/test_forum/phpBB3/app.php/restApiV1/boards/get"

intents = discord.Intents.all()
#import asyncpg
timer_moment = time_dt(hour=16,minute=47)
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

MY_GUILD = discord.Object(id=309746672056008706)  # replace with your guild id
class MyBot(commands.Bot):
    def __init__(self, *, command_prefix: str,intents: discord.Intents):
        super().__init__(command_prefix=command_prefix,intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        #self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
# =============================================================================
#     async def setup_hook(self):
#         # This copies the global commands over to your guild.
#         self.tree.copy_global_to(guild=MY_GUILD)
#         await self.tree.sync(guild=MY_GUILD)
# =============================================================================

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#client = discord.Client(intents=intents)

bot = MyBot(command_prefix='G!',intents=intents)
                        
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
    # sendTableStatus.start()
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

@bot.command(name='get-table')
@commands.has_role('Guildien')
async def get_table(ctx):
    if ctx.channel.name == "test_bot":
        response = requests.get(api_url)
        data = response.json()
        Current_Date = time.gmtime()
        partie = []
        for key,d in data.items():
            print(key)
            d['date'] = time.strptime(key,'%d%m%Y')
            partie.append(d)
        partie = [p for p in partie if p['date']>= Current_Date]
        print(partie)
        msg = json.dumps(partie)
        await ctx.channel.send(msg+ "" + ctx.author.mention)
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
    
@bot.hybrid_command()
async def testhybrid(ctx):
    await ctx.send("This is a hybrid command!")

@bot.tree.command()
@app_commands.describe(
    fruit='The first value you want to add something to',
)
async def fruits(interaction: discord.Interaction, fruit: str):
    await interaction.response.send_message(f'Your favourite fruit seems to be {fruit}')
@fruits.autocomplete('fruit')
async def fruits_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    fruits = ['Banana', 'Pineapple', 'Apple', 'Watermelon', 'Melon', 'Cherry']
    return [
        app_commands.Choice(name=fruit, value=fruit)
        for fruit in fruits if current.lower() in fruit.lower()
    ]
@tasks.loop(seconds=3.0,count=5)
async def sendTableStatus():
    print("loop valid")
    channel = bot.get_channel(967770476900413460)
    await channel.send("test message")
bot.run(TOKEN)
con.close()
