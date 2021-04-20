"""
Property of Sage L Mahmud (https://github.com/CactusDuud)
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

import discord
import os
import traceback
from datetime import datetime
from collections import defaultdict
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from dotenv import load_dotenv

# Get contents of .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_IDS = [614956261103894558]
PREFIX = '!'

# setting = None
table = None  # Represents the current probability generator (dice, deck, whatever)
# characters = defaultdict(dict)
# defaults = dict()

# Get that bot going!
bot = commands.Bot(command_prefix=PREFIX)
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {bot.user.name} has connected to \"{guild.name}\" (id:{guild.id})")


@bot.event
async def on_error(event, *args):
    with open('_error.log', 'a') as errorLog:
        if event == 'on_message':
            errorLog.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have permission to use this command.')


@slash.slash(name="ping", guild_ids=GUILD_IDS)
async def ping(ctx):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {ctx.author} called main._ping")
    await ctx.send(f"Pong! ({(bot.latency * 1000):.3f}ms)")


bot.load_extension("dice_and_deck_cog")
bot.load_extension("characters_cog")
bot.run(TOKEN)


"""
# ================================================= OPERATION COMMANDS =================================================

# TODO: Deprecated operator commands. Also separate you rat man! op_ prefix

@bot.command(name='op',
             aliases=['operator', 'dm'])
@commands.has_role('DM')
async def operator_commands(ctx, *cmds):
    global characters, IDcounter, defaults
    if cmds[0] == "csave" or cmds[0] == "character_save":
        with open("characters.dat", "wb") as dump:
            pickle.dump(characters, dump)
            pickle.dump(defaults, dump)
            pickle.dump(IDcounter, dump)
        print("Data written to \"characters.dat\"")
        await ctx.send(f"<@{ctx.author.id}>: Character data saved")
    elif cmds[0] == "cload" or cmds[0] == "character_load":
        try:
            with open("characters.dat", "rb") as dump:
                characters = pickle.load(dump)
                defaults = pickle.load(dump)
                IDcounter = pickle.load(dump)
            print("Data read from \"characters.dat\"")
            await ctx.send(f"<@{ctx.author.id}>: Character data loaded")
        except EOFError:
            await ctx.send(f"<@{ctx.author.id}>: **Error**: No save data")
    elif cmds[0] in ("cinfo", "c_info", "c_information"):
        cid = int(cmds[1]) if cmds[1] is not None else -1
        found = False
        if cid < 0:
            await ctx.send(f"<@{ctx.author.id}>: **Error**: Please provide a CID")
        else:
            for aid, cs in characters.items():
                if cid in characters[aid].keys():
                    found = True
                    await ctx.send(characters[aid][cid].info())
        if not found:
            await ctx.send(f"<@{ctx.author.id}>: **Error**: Character not found")
    elif cmds[0] in ("cedit", "c_edit"):
        cid = int(cmds[1]) if cmds[1] is not None else -1

        # Find the character
        chara = None
        for aid, cs in characters.items():
            if cid in characters[aid].keys():
                chara = characters[aid][cid]

        if chara is not None:
            if cid < 0:
                await ctx.send(f"<@{ctx.author.id}>: **Error**: Invalid CID")
            elif cmds[2] == 'appearance':
                chara.appearance = ' '.join(cmds[3:])
                await ctx.send(f"<@{ctx.author.id}>: "
                               f"Appearance of {chara.aliases[0]} "
                               f"{f'owned by <@{chara.owner}> ' if chara.owner != ctx.author.id else ''}"
                               f"updated")
            elif cmds[2] == 'attribute':
                try:
                    chara.attributes[cmds[3].upper()].base = int(cmds[4])
                    chara.refresh()
                    await ctx.send(f"<@{ctx.author.id}>: "
                                   f"{cmds[3].upper()} of {chara.aliases[0]} "
                                   f"{f'owned by <@{chara.owner}> ' if chara.owner != ctx.author.id else ''}"
                                   f"updated")
                except KeyError:
                    await ctx.send(f"<@{ctx.author.id}>: **Error**: Unknown attribute")
            elif cmds[2] in ('bday', 'birthday'):
                try:
                    date = [int(cmds[3]), int(cmds[4]), int(cmds[5])]
                    chara.bday = datetime(date[0], date[1], date[2])
                    # TODO: Refresh to calculate age based on setting
                    await ctx.send(f"<@{ctx.author.id}>: "
                                   f"Birthday of {chara.aliases[0]} "
                                   f"{f'owned by <@{chara.owner}> ' if chara.owner != ctx.author.id else ''}"
                                   f"updated")
                except ValueError:
                    await ctx.send(f"<@{ctx.author.id}>: **Error**: Improper date format\n"
                                   f"\tTry: `2000 9 21` (yyyy mm dd)")
            elif cmds[2] in ('bg', 'background'):
                chara.bg = ' '.join(cmds)
                await ctx.send(f"<@{ctx.author.id}>: "
                               f"Background of {chara.aliases[0]} "
                               f"{f'owned by <@{chara.owner}> ' if chara.owner != ctx.author.id else ''}"
                               f"updated")
            elif cmds[2] == 'biography':
                chara.biography = ' '.join(cmds[3:])
                await ctx.send(f"<@{ctx.author.id}>: "
                               f"Biography of {chara.aliases[0]} "
                               f"{f'owned by <@{chara.owner}> ' if chara.owner != ctx.author.id else ''}"
                               f"updated")
            elif cmds[2] == 'height':
                try:
                    chara.height = float(cmds[3])
                    await ctx.send(f"<@{ctx.author.id}>: "
                                   f"Height of {chara.aliases[0]} "
                                   f"{f'owned by <@{chara.owner}> ' if chara.owner != ctx.author.id else ''}"
                                   f"updated")
                except ValueError:
                    await ctx.send(f"<@{ctx.author.id}>: **Error**: Improper height format\n"
                                   f"\tTry: `1.75`")
            elif cmds[2] == 'rate':
                try:
                    chara.attributes[cmds[3].upper()].rate = float(cmds[4])
                    chara.refresh()
                    await ctx.send(f"<@{ctx.author.id}>: "
                                   f"{cmds[3].upper()} rate of {chara.aliases[0]} "
                                   f"{f'owned by <@{chara.owner}> ' if chara.owner != ctx.author.id else ''}"
                                   f"updated")
                except KeyError:
                    await ctx.send(f"<@{ctx.author.id}>: **Error**: Unknown attribute")
            elif cmds[2] == 'weight':
                try:
                    chara.weight = float(cmds[0])
                    await ctx.send(f"<@{ctx.author.id}>: "
                                   f"Weight of {chara.aliases[0]} "
                                   f"{f'owned by <@{chara.owner}> ' if chara.owner != ctx.author.id else ''}"
                                   f"updated")
                except ValueError:
                    await ctx.send(f"<@{ctx.author.id}>: **Error**: Improper weight format\n"
                                   f"\tTry: `62.55`")
            else:
                await ctx.send(f"<@{ctx.author.id}>: **Error**: Unknown character aspect")
        else:
            await ctx.send(f"<@{ctx.author.id}>: **Error**: Unknown character")
    elif cmds[0] in ("cdelete", "c_delete", "cdel", "cdelete"):
        cid = int(cmds[1]) if cmds[1] is not None else -1
        found = False

        # Find the character
        for aid, cs in characters.items():
            if cid in characters[aid].keys():
                found = True
                name = characters[aid][cid].aliases[0]
                owner = characters[aid][cid].owner
                del characters[aid][cid]

        if found:
            await ctx.send(f"<@{ctx.author.id}>: "
                           f"Appearance of {name} {f'owned by <@{owner}> ' if owner != ctx.author.id else ''} updated")
        else:
            await ctx.send(f"<@{ctx.author.id}>: **Error**: Invalid CID")
    else:
        await ctx.send(f"<@{ctx.author.id}>: **Error**: \"{' '.join(cmds)}\" not defined")
"""
