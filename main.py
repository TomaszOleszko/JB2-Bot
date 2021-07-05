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

options = [
    {
        "name": "start",
        "description": "Początek przedziału",
        "type": 4,
        "required": False
    },
    {
        "name": "stop",
        "description": "Koniec przedziału",
        "type": 4,
        "required": False
    }
]
options1 = [
    {
        "name": "dzien",
        "description": "Piwo dnia",
        "type": 5,
        "required": False,
    },
    {
        "name": "miesiac",
        "description": "Piwo miesiace",
        "type": 5,
        "required": False,
    }
]

emojis = {
    "pepeclown": "Rust",
    "pepeOK": "rocket",
    "pepeStab": "CSGO",
    "PepeYikes": "lol",
    "irizchuPat": "the simsy cztery"
}

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


@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 857969748931248159:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        role = discord.utils.get(guild.roles, name=emojis.get(payload.emoji.name))
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
        role = discord.utils.get(guild.roles, name=emojis.get(payload.emoji.name))
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
