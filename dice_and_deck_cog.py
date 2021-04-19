"""
dice_and_deck_cog.py
Property of Sage L Mahmud (https://github.com/CactusDuud)
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

# TODO: Categories in cogs (https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html)
# TODO: Migrate "dice cup" rolls
# TODO: Refactor help text to include decks

import dice
import discord
import traceback
from datetime import datetime
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

GUILD_IDS = [614956261103894558]


class DiceAndDeck(commands.Cog,
                  name="Dice and Deck Cog",
                  description="Dice rolls and deck draws; anything using chance."):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="cogtest", guild_ids=GUILD_IDS)
    async def _test(self, ctx: SlashContext):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {ctx.author} called main._test")
        await ctx.send("test")

    @cog_ext.cog_slash(name='roll',
                       description='Rolls the given die (Ex: 1d6). '
                                   'Modifiers are, in order: general modifiers, math, comparisons.',
                       guild_ids=GUILD_IDS,
                       options=[
                           create_option(
                               name="roll_string",
                               description="The string to generate a roll. Defaults to 1d100.",
                               option_type=3,
                               required=False
                           )
                       ])
    async def roll(self, ctx, roll_string: str = '1d100'):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {ctx.author} called DiceAndDeck.roll with "
              f"\"{roll_string.lower()}\"")
        try:
            global table
            table = dice.Dice(roll_string.lower())
            table.roll()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] \tresulted in \"{table.results()}\"")
            await ctx.send(f"<@{ctx.author.id}>'s {table}:\n\t{table.results()}")
        except dice.DiceException as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] \terror \"{e}\"")
            await ctx.send(f"<@{ctx.author.id}>: **Error**: {e}")
        except Exception as e:
            traceback.print_exc()
            await ctx.send(f"<@{ctx.author.id}>: **Error**: {e}")


def setup(bot):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] dice_and_deck_cog initialised...")
    bot.add_cog(DiceAndDeck(bot))


"""
class DiceAndDeck(commands.Cog,
                  name="Dice and Decks",
                  description="Dice rolls and deck draws; anything using chance."):

    @commands.command(name='reroll',
                      aliases=['re-roll', 'rr'],
                      help='Re-rolls the last die thrown.')
    async def reroll(self, ctx):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {ctx.author} called discord_dice.reroll")
        global table
        try:
            if type(table) == dice.Dice:
                table.roll()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] \tresult \"{table.results()}\"")
                await ctx.send(f"<@{ctx.author.id}>'s {table}:\n\t{table.results()}")
            # elif type(table) is card_deck.Deck:
            # await ctx.send(f"<@{ctx.author.id}>: **Error**: Deck can't be rolled\n\tTry `{PREFIX}deck_draw`")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] \terror no dice on table")
                await ctx.send(f"<@{ctx.author.id}>: **Error**: No previous rolls")
        except dice.DiceException as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] \terror \"{e}\"")
            await ctx.send(f"<@{ctx.author.id}>: **Error**: {e}")
        except Exception as e:
            traceback.print_exc()
            await ctx.send(f"<@{ctx.author.id}>: **Error**: {e}")

    @commands.command(name='reprint',
                      aliases=['re-print', 'rp'],
                      help='Reprints the last roll result.')
    async def reprint(self, ctx):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {ctx.author} called discord_dice.reprint")
        global table
        try:
            if type(table) == dice.Dice:
                await ctx.send(f"<@{ctx.author.id}>'s {table}:\n\t{table.results()}")
                # await ctx.send(f"<@{ctx.author.id}>'s {table} card: {table.results()}")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] \terror no dice on table")
                await ctx.send(f"<@{ctx.author.id}>: **Error**: No previous rolls")
        except dice.DiceException as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] \terror \"{e}\"")
            await ctx.send(f"<@{ctx.author.id}>: **Error**: {e}")
        except Exception as e:
            traceback.print_exc()
            await ctx.send(f"<@{ctx.author.id}>: **Error**: {e}")

    @commands.command(name='current_die',
                      aliases=['current_dice', 'currentdie', 'currentdice',
                               'current_deck', 'currentdeck', 'print_current', 'cd'],
                      help='Prints the type of die that has just been rolled.')
    async def print_current(self, ctx):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {ctx.author} called discord_dice.print_current")
        global table
        try:
            if type(table) == dice.Dice:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] \tresult \"{table}\"")
                await ctx.send(f"<@{ctx.author.id}>: The current die is {table}")
                # await ctx.send(f"<@{ctx.author.id}>: The current deck is a(n) {table}")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] \terror no dice on table")
                await ctx.send(f"<@{ctx.author.id}>: **Error**: No current die")
        except dice.DiceException as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] \terror \"{e}\"")
            await ctx.send(f"<@{ctx.author.id}>: **Error**: {e}")
        except Exception as e:
            traceback.print_exc()
            await ctx.send(f"<@{ctx.author.id}>: **Error**: {e}")

    @commands.command(name='deck',
                      aliases=['d'],
                      help='Creates a new deck of cards.')
    async def deck(self, ctx, cmd: str = 'standard', num: int = 1):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {ctx.author} called discord_dice.deck")
        global table
        try:
            table = card_deck.Deck(cmd.lower())
            table.draw(num)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] \tresult \"{table}\"")
            await ctx.send(f"<@{ctx.author.id}> created a new {table} and drew:\n"
                           f"{table.result(num)}")
        except dice.DiceException as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] \terror \"{e}\"")
            await ctx.send(f"<@{ctx.author.id}>: **Error**: {e}")
        except Exception as e:
            traceback.print_exc()
            await ctx.send(f"<@{ctx.author.id}>: **Error**: {e}")

    @commands.command(name='deck_draw',
                      aliases=['deckdraw', 'dd'],
                      help='Draws from the current deck of cards')
    async def deck_draw(self, ctx, num: int = 1):
        global table
        if type(table) is card_deck.Deck:
            if 0 < num <= len(table):
                table.draw(num)
                await ctx.send(f"<@{ctx.author.id}>'s {table} card{'s are' if num > 1 else ' is'}:\n"
                               f"{table.results(num)}")
            else:
                await ctx.send(f"<@{ctx.author.id}>: **Error**: Not enough cards in deck\n"
                               f"\tTry `{PREFIX}deck_reshuffle`")
        elif type(table) in (dice.Dice, fudge.Dice):
            await ctx.send(f"<@{ctx.author.id}>: **Error**: Dice can't be drawn from\n"
                           f"\tTry `{PREFIX}reroll`")
        else:
            await ctx.send(f"<@{ctx.author.id}>: **Error**: No current deck")

    @commands.command(name='deck_reshuffle',
                      aliases=['dr', 'deckreshuffle', 'deck_shuffle', 'deckshuffle'],
                      help='Restores the deck to its initial state')
    async def reshuffle(self, ctx):
        global table
        if type(table) is card_deck.Deck:
            table.reshuffle()
            await ctx.send(f"<@{ctx.author.id}> reshuffled the {table}")
        elif type(table) in (dice.Dice, fudge.Dice):
            await ctx.send(f"<@{ctx.author.id}>: **Error**: Dice can't be shuffled\n")
        else:
            await ctx.send(f"<@{ctx.author.id}>: **Error**: No current deck")

    @commands.command(name='deck_count',
                      aliases=['dc', 'deckcount'],
                      help='Prints the number of cards remaining in the current deck')
    async def deck_count(self, ctx):
        global table
        if type(table) is card_deck.Deck:
            await ctx.send(f"<The current {table} has "
                           f"{len(table)} card{'s' if len(table) != 1 else ''} remaining")
        elif type(table) in (dice.Dice, fudge.Dice):
            await ctx.send(f"<@{ctx.author.id}>: **Error**: Dice don't have remaining cards\n"
                           f"\tTry `{PREFIX}current_die`")
        else:
            await ctx.send(f"<@{ctx.author.id}>: **Error**: No current deck")
"""
