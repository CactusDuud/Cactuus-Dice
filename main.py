"""
Property of Sage L Mahmud (https://github.com/CactusDuud)
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
https://creativecommons.org/licenses/by-nc-sa/4.0/
"""
import character
import deck as card_deck
import dice
import discord
import fudge
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
# table = None  # Represents the current probability generator (dice, deck, whatever) TODO: is this even necessary?
# characters = defaultdict(dict)
# defaults = dict()
# IDcounter = 0  # TODO: Use SQL to better separate IDs? There's a better way at least

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
async def _ping(ctx):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {ctx.author} called main._ping")
    await ctx.send(f"Pong! ({(bot.latency * 1000):.3f}ms)")


bot.load_extension("dice_and_deck_cog")
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



# ===================================================== CHARACTERS =====================================================


@bot.command(name='character_create',
             aliases=['cc', 'charactercreate', 'create_character', 'createcharacter'],
             help='Creates a new character (Ex: Orc Jorhas Smirathu)')
async def character_create(ctx, race: str, *name: str):
    global IDcounter
    if name and race:
        try:
            characters[ctx.author.id][IDcounter] = \
                character.Character(ctx.author.id, IDcounter, ' '.join(name), race.capitalize())
            await ctx.send(f"<@{ctx.author.id}>: New character created!\n"
                           f"\tCID: {characters[ctx.author.id][IDcounter].cid}\n"
                           f"\tName: {characters[ctx.author.id][IDcounter].aliases[0]}\n"
                           f"\tRace: {characters[ctx.author.id][IDcounter].race}")
            IDcounter += 1
        except KeyError:
            await ctx.send(f"<@{ctx.author.id}>: **Error**: Invalid Race")
        except Exception as e:
            print(e)
    elif not name:
        await ctx.send(f"<@{ctx.author.id}>: **Error**: New character requires a name")
    elif not race:
        await ctx.send(f"<@{ctx.author.id}>: **Error**: New character requires a race")
    else:
        await ctx.send(f"<@{ctx.author.id}>: **Error**: New character requires a name and race"
                       f"\tEx: `>>character_create Human Finn`")


@bot.command(name='character_assign',
             aliases=['ca', 'characterassign', 'character_assign_points', 'characterassignpoints'],
             help='Assigns attribute points to a character')
async def character_assign(ctx, cid: int = -1, *points: int):
    # Consult defaults
    if ctx.author.id in defaults.keys() and cid <= 0:
        cid = defaults[ctx.author.id]

    if cid >= 0 and len(points) >= 9:
        try:
            chara = characters[ctx.author.id][cid]
            if chara.attr_points > 0:
                result = chara.assign(points[:9])
                if result:
                    await ctx.send(f"<@{ctx.author.id}>: Points assigned! ({chara.attr_points} remaining)\n"
                                   f"{chara.info('attributes')}")
                else:
                    await ctx.send(f"<@{ctx.author.id}>: **Error**: "
                                   f"Invalid point total ({chara.attr_points} remaining)")
            else:
                await ctx.send(f"<@{ctx.author.id}>: No points remaining)")
        except KeyError:
            await ctx.send(f"<@{ctx.author.id}>: **Error**: Character not found. Check CID.")
    elif len(points) != 9:
        await ctx.send(f"<@{ctx.author.id}>: **Error**: Too few arguments for assignment")
    else:
        await ctx.send(f"<@{ctx.author.id}>: **Error**: Invalid CID")


@bot.command(name='character_update',
             aliases=['cu', 'characterupdate', 'copper'],
             help='Updates character info via CID')
async def character_update(ctx, cmd: str, cid: int = -1, *cmds: str):
    if cid < 0:
        await ctx.send(f"<@{ctx.author.id}>: **Error**: Invalid CID")
    elif cmd == 'appearance':
        characters[ctx.author.id][cid].appearance = ' '.join(cmds)
        await ctx.send(f"<@{ctx.author.id}>: Appearance of {characters[ctx.author.id][cid].aliases[0]} updated")
    elif cmd in ('bday', 'birthday'):
        try:
            date = [int(cmds[0]), int(cmds[1]), int(cmds[2])]
            characters[ctx.author.id][cid].bday = datetime(date[0], date[1], date[2])
            # TODO: Refresh to calculate age based on setting
            await ctx.send(f"<@{ctx.author.id}>: Birthday of {characters[ctx.author.id][cid].aliases[0]} updated")
        except ValueError:
            await ctx.send(f"<@{ctx.author.id}>: **Error**: Improper date format\n"
                           f"\tTry: `2000 9 21` (yyyy mm dd)")
    elif cmd in ('bg', 'background'):
        characters[ctx.author.id][cid].bg = ' '.join(cmds)
        await ctx.send(f"<@{ctx.author.id}>: Background of {characters[ctx.author.id][cid].aliases[0]} updated")
    elif cmd == 'biography':
        characters[ctx.author.id][cid].biography = ' '.join(cmds)
        await ctx.send(f"<@{ctx.author.id}>: Biography of {characters[ctx.author.id][cid].aliases[0]} updated")
    elif cmd == 'height':
        try:
            characters[ctx.author.id][cid].height = float(cmds[0])
            await ctx.send(f"<@{ctx.author.id}>: Height of {characters[ctx.author.id][cid].aliases[0]} updated")
        except ValueError:
            await ctx.send(f"<@{ctx.author.id}>: **Error**: Improper height format\n"
                           f"\tTry: `1.75`")
    elif cmd == 'weight':
        try:
            characters[ctx.author.id][cid].weight = float(cmds[0])
            await ctx.send(f"<@{ctx.author.id}>: Weight of {characters[ctx.author.id][cid].aliases[0]} updated")
        except ValueError:
            await ctx.send(f"<@{ctx.author.id}>: **Error**: Improper weight format\n"
                           f"\tTry: `62.55`")
    else:
        await ctx.send(f"<@{ctx.author.id}>: **Error**: Unknown character aspect")


@bot.command(name='character_default',
             aliases=['cdef', 'characterdefault'],
             help='Sets a default character for your commands by CID')
async def character_default(ctx, cid: int = -1):
    try:
        if type(cid) is not int:
            raise ValueError
        if cid < 0:
            await ctx.send(
                f"<@{ctx.author.id}>: Default removed: "
                f"{characters[ctx.author.id][defaults[ctx.author.id]].aliases[0]} "
                f"(CID:{characters[ctx.author.id][defaults[ctx.author.id]].cid})")
            defaults[ctx.author.id] = -1
        else:
            chara = characters[ctx.author.id][cid]
            defaults[ctx.author.id] = cid
            await ctx.send(f"<@{ctx.author.id}>: Default assigned: {chara.aliases[0]} (CID:{chara.cid})")
    except KeyError:
        await ctx.send(f"<@{ctx.author.id}>: **Error**: Invalid CID")
    except ValueError:
        await ctx.send(f"<@{ctx.author.id}>: **Error**: Invalid CID")


@bot.command(name='character_info',
             aliases=['ci', 'characterinfo', 'character_status', 'characterstatus'],
             help='Prints info on a character of yours (Ex: all Johan Napach)')
async def character_info(ctx, mode: str, *name: str):
    full_name = ' '.join(name)
    cid = -1

    # Consult defaults
    if ctx.author.id in defaults.keys() and cid <= 0:
        cid = defaults[ctx.author.id]
    else:
        # Find an ID
        matches = []
        for dict_id, dict_chara in characters[ctx.author.id].items():
            for a in dict_chara.aliases:
                if full_name in a:
                    matches += [dict_chara]
                    cid = dict_id if len(matches) == 1 else -1

        if len(matches) > 1:
            for match in matches:
                await ctx.send(f"<@{ctx.author.id}>: Possible character: {match.aliases[0]} (CID:{match.cid})")

    if cid >= 0:
        try:
            chara = characters[ctx.author.id][cid]
            if mode in ('all', 'attributes', 'bio', 'status'):
                await ctx.send(f"{chara.info(mode)}")
            else:
                await ctx.send(f"<@{ctx.author.id}>: **Error**: Invalid info mode\n"
                               f"\tTry `all`, `bio`, or `status` before the name")
        except KeyError:
            await ctx.send(f"<@{ctx.author.id}>: **Error**: Invalid CID")

    else:
        await ctx.send(f"<@{ctx.author.id}>: **Error**: Character not found")


@bot.command(name='character_info_id',
             aliases=['cii', 'characterinfoid', 'character_status_id', 'characterstatusid'],
             help='Prints info on a character of yours via CID (Ex: 1337)')
async def character_info_id(ctx, mode: str, cid: int = -1, ):
    # Consult defaults
    if ctx.author.id in defaults.keys() and cid <= 0:
        cid = defaults[ctx.author.id]

    try:
        if cid < 0:
            raise ValueError
        chara = characters[ctx.author.id][cid]
        if mode in ('all', 'attributes', 'bio', 'status'):
            await ctx.send(f"{chara.info(mode)}")
        else:
            await ctx.send(f"<@{ctx.author.id}>: **Error**: Invalid info mode"
                           f"\tTry `mode='all'`, `mode='bio'`, or `mode='status'`")
    except KeyError:
        await ctx.send(f"<@{ctx.author.id}>: **Error**: Unknown character")
    except ValueError:
        await ctx.send(f"<@{ctx.author.id}>: **Error**: Invalid CID")


@bot.command(name='character_observe',
             aliases=['co', 'characterobserve', 'character_look', 'characterlook'],
             help='Prints info on a certain character (Ex: Johan cid=1337)')
async def character_observe(ctx):
    await ctx.send(f"<@{ctx.author.id}>: **Error**: 'character_observe' not yet implemented")
    # TODO: Implement observation


@bot.command(name='character_identify',
             aliases=['cid', 'characteridentify', 'character_id', 'characterid'],
             help='Prints the id of a character (Ex: Johan Napach)')
async def character_identify(ctx, *name: str):
    full_name = ' '.join(name)
    cid = -1

    # Find an ID
    matches = []
    for dict_id, dict_chara in characters[ctx.author.id].items():
        for a in dict_chara.aliases:
            if full_name in a:
                matches += [dict_chara]
                cid = dict_id if len(matches) == 1 else -1

    if len(matches) > 1:
        for match in matches:
            await ctx.send(f"<@{ctx.author.id}>: Possible character: {match.aliases[0]} (CID:{match.cid})")

    if cid >= 0:
        try:
            chara = characters[ctx.author.id][cid]
            await ctx.send(f"<@{ctx.author.id}>: "
                           f"{chara.aliases[0]}'{'' if chara.aliases[0][-1] == 's' else 's'} CID:{chara.cid}")
        except KeyError:
            await ctx.send(f"<@{ctx.author.id}>: **Error**: Invalid CID")

    else:
        await ctx.send(f"<@{ctx.author.id}>: **Error**: Character not found. Try providing a CID.")
"""