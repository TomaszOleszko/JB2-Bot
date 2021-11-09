import os
import random
import json
from datetime import date

import discord
from discord_slash import SlashCommand, SlashContext

SERVER_ID = 636164373970157578

intents = discord.Intents.all()
client = discord.Client(intents=intents)
slash = SlashCommand(client, sync_commands=True)

with open('Data/config.json',encoding="utf8") as f:
  data = json.load(f) 


  
@slash.slash(name="Piwo", description="Piwo dnia i Piwo miesiąca", guild_ids=[SERVER_ID], options=data["piwa_options"])
async def guess(ctx: SlashContext, dzien=True, miesiac=False):
    date_tuple = date.today().timetuple()
    if not dzien and not miesiac:
        await ctx.send(content="Brak piwska")
    if dzien:
        random.seed(date_tuple[1] * 100 + date_tuple[2] * 50)
        piwo = random.choice(data["piwa"])
        await ctx.send(content=f"Piwo dnia --> "+os.path.splitext(piwo)[0], file=discord.File("piwa/"+piwo))
    if miesiac:
        random.seed(date_tuple[1] * 1000)
        piwo = random.choice(data["piwa"])
        await ctx.send(content=f"Piwo miesiąca --> "+os.path.splitext(piwo)[0], file=discord.File("piwa/"+piwo))


@slash.slash(name="zdam", description="Zdam czy nie zdam?", guild_ids=[SERVER_ID])
async def _test(ctx: SlashContext):
    await ctx.send(content="zdam",
                   embed=discord.Embed(title="ZDAJ CZY NIEZDAJ, OTO JEST PYTANIE...\n" + (random.choice(data["zdam_message_content"]))))


@slash.slash(name="Losu", description="Losowanko liczby", guild_ids=[SERVER_ID], options=data["losu_options"])
async def guess(ctx: SlashContext, start=0, stop=10):
    rand = random.randint(start, stop)
    await ctx.send(content=f"Losu Losu --> {rand}")

@slash.slash(name="AddProverb", description="Dodaje proverb podany es?",guild_ids=[SERVER_ID])
async def proverbs_geta(ctx, proverbik):
    f = open("prov.txt", "a", encoding='utf-8')
    proverb = proverbik
    if proverb.find('-') != -1 and proverb.find('-') != len(proverb)-1:
        proverb = "\n"+proverbik
        f.write(proverb)
        f.close
        await ctx.send(content=f"Dodano proverb:{proverb}")
    else:
        await ctx.send(content=f"podaj w formacie english version - polish version")

@slash.slash(name="DeleteProverb", description="Usuwa ostatnio dodany proverb es?",guild_ids=[SERVER_ID])
async def proverbs_geta(ctx):
    fd = open("prov.txt", "r")
    d = fd.read()
    fd.close()
    m = d.split("\n")
    s = "\n".join(m[:-1])
    fd = open("prov.txt", "w+")
    for i in range(len(s)):
        fd.write(s[i])
    fd.close()
    await ctx.send(content=f"usunieto i chuj")

@slash.slash(name="Proverbs", description="Zdaje angielski ez",guild_ids=[SERVER_ID])
async def proverbs_get(ctx: SlashContext):
    f = open('prov.txt', 'r', encoding='utf-8')
    # Reads a specific line of text in the file.
    proverbs = f.readlines()
    string = ""
    for _ in proverbs:
      string += _

    await ctx.send(content=string)




@client.event
async def on_raw_reaction_add(payload: object) -> object:
    message_id = payload.message_id
    if message_id == 857969748931248159:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        role = discord.utils.get(guild.roles, name=data["emojis"].get(payload.emoji.name))
        if role is not None:
            member = payload.member
            if member is not None:
                await member.add_roles(role)
                print("Użytkownik:", end=" ")
                print(member, end=" ")
                print("dodał rolę:", end=" ")
                print(role)
            else:
                print("member not found")
        else:
            print("role not found")


@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 857969748931248159:
        guild = client.get_guild(payload.guild_id)
        role = discord.utils.get(guild.roles, name=data["emojis"].get(payload.emoji.name))
        if role is not None:
            member = guild.get_member(payload.user_id)
            if member is not None:
                await member.remove_roles(role)
                print("Użytkownik:", end=" ")
                print(member, end=" ")
                print("USUNĄŁ rolę:", end=" ")
                print(role)
            else:
                print("member not found")
        else:
            print("role not found")


@client.event
async def on_ready():
    print("BOT RUNNING...")


client.run(os.getenv('DISCORD_TOKEN'))
