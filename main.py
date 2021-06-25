import os
from datetime import date
import random
import discord
from discord.ext import commands
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
        "required": False,
    },
    {
        "name": "stop",
        "description": "Koniec przedziału",
        "type": 4,
        "required": False,
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
piwa = [
    (
        'Kozel',
        'piwa/Kozel.png'
    ),
    (
        'Zatecki',
        'piwa/zatecky.jpeg'
    ),
    (
        'Namyslow',
        'piwa/namyslow.png'
    ),
    (
        'Warka',
        'piwa/Warka.png'
    ),
    (
        'Calsberg',
        'piwa/Carlsberg.png'
    )
]
emojis = {
    "pepeclown": "Rust",
    "pepeOK": "rocket",
    "pepeStab": "CSGO",
    "PepeYikes": "lol",
    "irizchuPat": "the simsy cztery"
}


@slash.slash(name="Piwo", description="Piwo dnia i Piwo miesiąca", guild_ids=[SERVER_ID], options=options1)
async def guess(ctx: SlashContext, dzien=True, miesiac=False):
    date_tuple = date.today().timetuple()
    if not dzien and not miesiac:
        await ctx.send(content="Brak piwska")
    if dzien:
        random.seed(date_tuple[1] + date_tuple[2])
        rand = random.choice(piwa)
        await ctx.send(content=f"Piwo dnia --> {rand[0]}", file=discord.File(rand[1]))
    if miesiac:
        random.seed(date_tuple[1])
        rand = random.choice(piwa)
        await ctx.send(content=f"Piwo miesiąca --> {rand[0]}", file=discord.File(rand[1]))


@slash.slash(name="zdam", description="Zdam czy nie zdam?", guild_ids=[SERVER_ID])
async def _test(ctx: SlashContext):
    if bool(random.getrandbits(1)):
        embed = discord.Embed(title="ZDAJ CZY NIEZDAJ, OTO JEST PYTANIE...\n  <:trolldog:801043177603727450>\n /|\ \n  "
                                    "/\ \nZAPRASZAMY W NASTĘPNYM ROKU...")
    else:
        embed = discord.Embed(
            title="ZDAJ CZY NIEZDAJ, OTO JEST PYTANIE...\n\ <:dogekek:801043201628700682> /\n     |\n   /\ \nJEDNAK "
                  "NIEZDAJ JEST MIŁOSIERNY... TYM RAZEM...")

    await ctx.send(content="zdam", embed=embed)


@slash.slash(name="Losu", description="Losowanko liczby", guild_ids=[SERVER_ID], options=options)
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
