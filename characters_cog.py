"""
characters_cog.py
Property of Sage L Mahmud (https://github.com/CactusDuud)
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

# TODO: use SQL to store characters

import character
import traceback
from datetime import datetime
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice
from sqlalchemy import create_engine

GUILD_IDS = [614956261103894558]


class CharactersCog(commands.Cog,
                    name="Dice and Deck Cog",
                    description="Dice rolls and deck draws; anything using chance."):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name='character_create',
                       description='Creates a new character.',
                       guild_ids=GUILD_IDS,
                       options=[
                           create_option(
                               name="ancestry",
                               description="What species and culture you come from.",
                               option_type=3,
                               required=True
                           ),
                           create_option(
                               name="character_name",
                               description="What species and culture you come from.",
                               option_type=3,
                               required=True
                           ),
                           create_option(
                               name="player",
                               description="Who the character is played by.",
                               option_type=6,
                               required=False
                           )
                       ])
    async def character_create(self, ctx, ancestry: str, character_name: str, player=None):
        try:
            player = ctx.author if ctx.author is None else player
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {ctx.author} called CharactersCog.character_create with:\n"
                  f"\t\t\tancestry:\t{ancestry}\n"
                  f"\t\t\tname:\t\t{character_name}\n"
                  f"\t\t\towner:\t\t{player}")

            new_character = character.Character(ancestry, character_name, player)

        except Exception as e:
            traceback.print_exc()
            await ctx.send(f"**Error**: {e}")

    # TODO: Update aliases, associated player, traits, stats, appearance, and bg


def setup(bot):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] characters_cog initialised...")
    bot.add_cog(CharactersCog(bot))


"""
# ===================================================== CHARACTERS =====================================================


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
