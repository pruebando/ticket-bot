import discord
from discord.ext import commands
import os
from webserver import keep_alive
import json
import asyncio
import random

intents = discord.Intents.default()
intents.members = True
intents.presences = True

client = commands.Bot(command_prefix='s!', intents=intents)

@client.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong! I have {(round(client.latency * 1000))} ms of latency.')
    
@client.event
async def on_ready():
    listau = ["Spying The Mods", "Spying Users", "Trolling Mods", "Doing Bad Bot Things", "Seeing Tickets", "Dm For Cool Bot Help"]
    await client.change_presence(activity=discord.Streaming(name=random.choice(listau), url="https://pene.com"))
    
    
 
@client.event
async def on_message(message):
 if message.guild is None and not message.author.bot:
     print("pene")
  
 await client.process_commands(message)

@client.listen()
async def on_message(message):
    if not message.guild and not message.author.bot:
        print(f"dm by {message.author.name}")
        with open("tickets.json", "r") as pene:
            kaka = 0
            pija = json.load(pene)
            for value in pija.keys():
                if pija[str(value)][0]==message.author.id:
                    embeddm=discord.Embed(description=f"{message.author.name} say:\n{message.content}", color=0xCC71DF)
                    await client.get_channel(pija[value][1]).send(embed = embeddm)
                    break
                kaka +=1
                if len(pija.keys()) == kaka:
                    a = await message.channel.send(embed=discord.Embed(description="React with 🔮 to open your ticket!", color=0xCC71DF))
                    await a.add_reaction("🔮")
                    
                    def check(reaction, user):
                     return user == message.author and str(reaction.emoji) == '🔮'

                    try:
                     reaction, user =      await client.wait_for('reaction_add', timeout=60.0, check=check)
                     print("ticket called")
                    except:
                        await message.channel.send("❌ Time of reaction is out")
                        raise
                    a = await client.get_guild(797082033318789181).create_text_channel(name=str(message.author.name), category=client.get_channel(797115849848258601))
                    await a.send(content="<@&797315822543831070>",embed=discord.Embed(description="⭐ <@&797315822543831070> An user has opened a new ticket! ⭐" , color=0xCC71DF))
                    
                    embeone = discord.Embed(description=":exclamation:Please wait to the staff team to answer you, they are not robots so it will take some time to answer:exclamation:", color=0xCC71DF)
                    
                    await message.channel.send(embed=embeone)
                    with open("tickets.json", "r") as paj:
                        popo = paj
                        pis = json.load(popo)
                        pis[f"ticket_{a.id}"] = [message.author.id, a.id]
                    with open ("tickets.json", "w") as papa:
                        ewe = papa.write(f"""{json.dumps(pis)}""")

@client.listen()
async def on_message(message):
    if message.guild is not None:
     if message.guild.id == 797082033318789181 and not message.author.bot:
      with open("tickets.json", "r") as a:
          auwu = json.load(a)
          for a in auwu.keys():
              if message.channel.id == auwu[a][1]:
                  embedchannel=discord.Embed(description =f"{message.author.name} says: \n{message.content}", color=0xCC71DF)
                  await client.get_user(auwu[a][0]).send(embed=embedchannel)
                  break 

@client.command(hidden=True, name="close")
async def close_ticket(ctx, *args):
    if not args:
     args = ''
    else:
     args = ' '.join(args)
    if ctx.message.guild.id == 797082033318789181:
        
     with open("tickets.json", "r") as yeye:
         asd = json.load(yeye)
         for xe in asd.keys():
             if asd[xe][1] == ctx.message.channel.id:
                 print("si")
                 aomebe=discord.Embed(description=f"Ticket closed! Reason: [{args}]", color=0xCC71DF)
                 await client.get_user(asd[xe][0]).send(embed=aomebe)
                 asd.pop(f"ticket_{ctx.channel.id}", None )
                 with open("tickets.json", "w") as awa:
                  json.dump(asd, awa)
                  await ctx.send(embed=aomebe)
                  await asyncio.sleep(6)
                  await ctx.channel.delete()                
                  break
             else:
                 print('a')
        

@client.command()
async def about(ctx):
    ao = discord.Embed(title="Hi, i am a bot only for this server created to help the server!\nmy owner is orainge#5151 and the dev team people now are \n \norainge#5151", color=0xCC71DF, timestamp=ctx.message.created_at)
  
    await ctx.send(embed=ao)
    
@client.command()
async def info(ctx):
 await ctx.send(embed=discord.Embed(description="**Hello! I am Saturn Advertising’s Bot! I was programmed to keep the server safe and manage modmail. If you spot a bug, contact through my modmail! I am managed by the Technical Team.**", color=0xCC71DF, timestamp=ctx.message.created_at))

@client.command(hidden=True)
@commands.is_owner()
async def say(ctx, *args):
    await ctx.message.delete()
    await ctx.send(' '.join(args))



cogs = ["admin",]
for i in cogs:
 client.load_extension(i)
 
keep_alive()

client.run(str(os.getenv('TOKEN')))
