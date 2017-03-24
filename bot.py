"""A python script to create interactivity in discord."""

import random
from discord.ext import commands
import discord
import json
import logging
import re

description = """
Hello! I am a bot written by Tom to provide some nice utilities and banter.
"""

logger = logging.getLogger('discord')
logger.setLevel(logging.CRITICAL)
handler = logging.FileHandler(
    filename='discordBot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

prefix = ['?', '!']
bot = commands.Bot(command_prefix=prefix, description=description)


@bot.event
async def on_ready():
    print('Logged in as:')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    print('------')


@bot.event
async def on_resumed():
    print('resumed...')


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if "sirknight" in message.content.lower().split():
        msg = 'Speaking of Sirknight, he still needs to 1v1 Bethan'
        await bot.send_message(message.channel, msg)

    if "bethan" in message.content.lower().split():
        msg = 'HELLO {0.author.mention}, I HEARD U MENTIONED MY FAV, BETHAN'.format(
            message)
        await bot.send_message(message.channel, msg)

    if "josh" in message.content.lower().split():
        msg = 'Jishwa is my daddy...'
        await bot.send_message(message.channel, msg)

    if "jack" in message.content.lower().split():
        msg = '<:jack:265554341077712896>'
        await bot.send_message(message.channel, msg)

    if "penis" in message.content.lower().split():
        ran = random.randint(1, 3)
        if ran == 1:
            await bot.add_reaction(message, "🍆")
        elif ran == 2:
            await bot.add_reaction(message, "🍆")
            await bot.add_reaction(message, "💦")
        elif ran == 3:
            await bot.add_reaction(message, "🍆")
            await bot.add_reaction(message, "💦")
            await bot.add_reaction(message, "👅")

    if message.content.startswith('?guess'):
        await bot.send_message(message.channel,
                               'Guess a number between 1 to 10')

        def guess_check(m):
            return m.content.isdigit()

        guess = await bot.wait_for_message(timeout=5.0, author=message.author, check=guess_check)
        answer = random.randint(1, 10)
        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'
            await bot.send_message(message.channel, fmt.format(answer))
            return
        if int(guess.content) == answer:
            await bot.send_message(message.channel, 'You are right!')
        else:
            await bot.send_message(message.channel, 'Sorry. It is actually {}.'.format(answer))

    await bot.process_commands(message)


@bot.command()
async def add(left: int, right: int):
    """Adds two numbers together."""
    await bot.say(left + right)


@bot.command()
async def git():
    """Sends Discord-board-game repo link."""
    await bot.say('https://github.com/Skidushe/Discord-board-game')


@bot.command()
async def pruned(daysgiven: int):
    """Sends estimated members to be pruned."""
    a = await bot.estimate_pruned_members(bot.get_server(server_id), days=int(daysgiven))
    await bot.say(a)


# def remRedunCol(ctx, roleComp):
#     for role in ctx.message.author.roles:
#         if role.name.startswith('#') and role.name != roleComp.name:
#             await bot.remove_roles(ctx.message.author, role)


@bot.command(pass_context=True)
async def colour(ctx, hex: str):
    """Sets the person's in chat colour."""
    hex = hex.upper()
    restring = re.compile(r"^#[0-9A-F]{6}$")
    match = re.search(restring, hex)
    if match:
        col = int(str(hex.lstrip('#').upper()), 16)
        serverRoles = bot.get_server(server_id)
        getRole = discord.utils.get(serverRoles.roles, name=hex)
        if discord.utils.get(serverRoles.roles, name=hex) is None:
            newcolrole = await bot.create_role(bot.get_server(server_id), name=hex, mentionable=False, colour=discord.Colour(col))
            await bot.add_roles(ctx.message.author, newcolrole)
            await bot.move_role(bot.get_server(server_id), newcolrole, (len(bot.get_server(server_id).roles) - 2))
            newrole = discord.utils.get(
                bot.get_server(server_id).roles, name=hex)
            await bot.say("Created new role named " + str(newrole.name) + " ID: " + str(newrole.id))
            # remRedunCol(ctx, newcolrole)
            for role in ctx.message.author.roles:
                if (role.name.startswith('#')) and (role.name != newrole.name):
                    await bot.remove_roles(ctx.message.author, role)
        else:
            newrole = discord.utils.get(
                bot.get_server(server_id).roles, name=hex)
            for role in ctx.message.author.roles:
                if (role.name.startswith('#')) and (role.name != newrole.name):
                    await bot.remove_roles(ctx.message.author, role)
            await bot.say("This colour already exists, added to existing group.")
            await bot.add_roles(ctx.message.author, getRole)
    else:
        await bot.say(hex + " is not in the hex form #A1B2C3.")

@bot.command(pass_context=True)
async def removeRedundantColours(ctx):
    """Sends the issuers id, roles."""
    for role in bot.get_server(server_id).roles:
        memberswithrole = 0
        for member in bot.get_server(server_id).members:
            if role in member.roles:
                memberswithrole += 1
        if memberswithrole == 0:
            print(str(role.name))
            restring = re.compile(r"^#[0-9A-F]{6}$")
            match = re.search(restring, role.name)
            if match:
                await bot.delete_role(bot.get_server(server_id), role)

@bot.command(pass_context=True)
async def IDList(ctx):
    """Sends the issuers id, roles."""
    await bot.say(ctx.message.author)
    await bot.say(ctx.message.author.roles)


@bot.command(pass_context=True)
async def rolePos(ctx, roleName: str):
    """Sends the position value of the role."""
    await bot.say(discord.utils.get(bot.get_server(server_id).roles, name=roleName).position)

@bot.command(pass_context=True)
async def insultMe(ctx, member: discord.Member = None):
    """Sends an insult about the sender."""
    if member is None:
        member = ctx.message.author
    insults = open("Insult.txt", 'r')
    insultsArray = []
    for line in insults:
        insultsArray.append(str(line))
    ran = random.randint(1, len(insultsArray))
    await bot.say('{0}'.format(member)+" "+str(insultsArray[ran]))


@bot.command(pass_context=True)
async def roleColours(ctx):
    """Prints all roles and their respective colours"""
    block = ""
    for role in bot.get_server(server_id).roles:
        block += str(str(role.name) + " : " + str(role.colour.value) +
                     " / " + str(role.colour.to_tuple()) + "\n")
    await bot.say(("`" * 3) + block + ("`" * 3))


@bot.command()
async def roll(dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
        if rolls > 100:
            await bot.say('Number too big.')
            raise ValueError('Dice numbers too big.')
        if limit > 100:
            await bot.say('Number too big.')
            raise ValueError('Dice numbers too big.')
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices: str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))


@bot.command()
async def joined(member: discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))


def load_credentials():
    with open('credentials.json') as f:
        return json.load(f)


if __name__ == '__main__':
    credentials = load_credentials()
    token = credentials['token']
    server_id = credentials['server_id']
    bot.client_id = credentials['client_id']

bot.run(token)