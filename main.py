from datetime import date
import random
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

TOKEN = 
SERVER_ID = 

client = commands.Bot(command_prefix='!')
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
piwa = [
    (
        'Kozel',
        'piwa/Kozel_lezak.png'
    ),
    (
        'Zatecki',
        'piwa/zatecky-svetly-lezak.jpg'
    ),
    (
        'Namyslow',
        'piwa/namyslow-butelka.jpg'
    ),
    (
        'Warka',
        'piwa/Warka-classic_but_OK.png'
    ),
    (
        'Calsberg',
        'piwa/67746.jpg'
    )
]


@slash.slash(name="Piwo", description="Piwo dnia", guild_ids=[SERVER_ID])
async def guess(ctx: SlashContext):
    date_tuple = date.today().timetuple()
    random.seed(date_tuple[1]+date_tuple[2])
    rand = random.choice(piwa)
    await ctx.send(content=f"Piwo dnia --> {rand[0]}", file=discord.File(rand[1]))


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
async def on_ready():
    print("BOT RUNNING...")


client.run(TOKEN)
