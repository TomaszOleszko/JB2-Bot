import random
import discord

TOKEN = ""
SERVER_ID = 

client = discord.Client()


komendy = "Komendy:\n.zdam?\n"


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("/help"):
        await message.channel.send(komendy)
        return
    if message.content.startswith("/zdam?"):
        if bool(random.getrandbits(1)):
            await message.channel.send(
                "ZDAJ CZY NIEZDAJ, OTO JEST PYTANIE...\n <:trolldog:801043177603727450>\n /|\ \n  /\ \nZAPRASZAMY W NASTĘPNYM ROKU...")
            return
        else:
            await message.channel.send(
                "ZDAJ CZY NIEZDAJ, OTO JEST PYTANIE...\n\ <:dogekek:801043201628700682> /\n     |\n   /\ \nJEDNAK NIEZDAJ JEST MIŁOSIERNY... TYM RAZEM...")
            return


@client.event
async def on_ready():
    print("BOT RUNNING...")


client.run(TOKEN)
