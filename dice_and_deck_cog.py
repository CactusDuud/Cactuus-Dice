"""
dice_and_deck_cog.py
Property of Sage L Mahmud (https://github.com/CactusDuud)
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

# TODO: Migrate to "dice cup" rolls

import deck as card_deck
import dice
import traceback
from datetime import datetime
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

GUILD_IDS = [614956261103894558]


class DiceAndDeckCog(commands.Cog,
                     name="Dice and Deck Cog",
                     description="Dice rolls and deck draws; anything using chance."):
    def __init__(self, bot):
        self.bot = bot

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
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {ctx.author} called DiceAndDeckCog.roll with "
              f"\"{roll_string.lower()}\"")
        try:
            global table
            table = dice.Dice(roll_string.lower())
            table.roll()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] \tresulted in \"{table.results()}\"")
            await ctx.send(f"{ctx.author.display_name}'s {table}:\n\t{table.results()}")
        except dice.DiceException as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] \terrored \"{e}\"")
            await ctx.send(f"**Error**: {e}")
        except Exception as e:
            traceback.print_exc()
            await ctx.send(f"**Error**: {e}")

    @cog_ext.cog_slash(name='reroll',
                       description='Re-rolls the last dice thrown.',
                       guild_ids=GUILD_IDS)
    async def reroll(self, ctx):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {ctx.author} called DiceAndDeckCog.reroll")
        global table
        try:
            if type(table) is dice.Dice:
                table.roll()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] \tresulted in \"{table.results()}\"")
                await ctx.send(f"{ctx.author.display_name}'s {table}:\n\t{table.results()}")
            # elif type(table) is card_deck.Deck:
            # await ctx.send(f"<@{ctx.author.id}>: **Error**: Deck can't be rolled\n\tTry `{PREFIX}deck_draw`")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] \terrored \"no dice on table\"")
                await ctx.send(f"**Error**: No previous rolls")
        except dice.DiceException as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] \terrored \"{e}\"")
            await ctx.send(f"**Error**: {e}")
        except Exception as e:
            traceback.print_exc()
            await ctx.send(f"**Error**: {e}")

    @cog_ext.cog_slash(name='reprint',
                       description='Resends the last roll result.',
                       guild_ids=GUILD_IDS)
    async def reprint(self, ctx):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {ctx.author} called DiceAndDeckCog.reprint")
        global table
        try:
            if type(table) is dice.Dice:
                await ctx.send(f"{ctx.author.display_name}'s last {table}:\n\t{table.results()}")
                # await ctx.send(f"<@{ctx.author.id}>'s {table} card: {table.results()}")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] \terrored \"no dice on table\"")
                await ctx.send(f"**Error**: No previous rolls")
        except dice.DiceException as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] \terrored \"{e}\"")
            await ctx.send(f"**Error**: {e}")
        except Exception as e:
            traceback.print_exc()
            await ctx.send(f"**Error**: {e}")

    @cog_ext.cog_slash(name='table',
                       description='Prints what is on the table.',
                       guild_ids=GUILD_IDS)
    async def print_table(self, ctx):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {ctx.author} called DiceAndDeckCog.print_table")
        global table
        try:
            if type(table) is dice.Dice:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] \ttable is \"{table}\"")
                await ctx.send(f"{table} is currently on the table.")
            elif type(table) is card_deck.Deck:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] \ttable is \"{table}\"")
                await ctx.send(f"{table} is currently on the table."
                               f"\t{len(table)} card{'s' if len(table) != 1 else ''} remaining")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] \terrored \"no dice on table\"")
                await ctx.send(f"**Error**: No current die")
        except dice.DiceException as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] \terrored \"{e}\"")
            await ctx.send(f"**Error**: {e}")
        except Exception as e:
            traceback.print_exc()
            await ctx.send(f"**Error**: {e}")

    @cog_ext.cog_slash(name='deck',
                       description='Creates a new deck of cards and draws a card.',
                       guild_ids=GUILD_IDS,
                       options=[
                           create_option(
                               name="type",
                               description="The deck type. Defaults to standard 52-card deck.",
                               option_type=3,
                               required=False,
                               choices=[
                                   create_choice(
                                       name="standard",
                                       value="52"
                                   ),
                                   create_choice(
                                       name="standard+",
                                       value="53"
                                   ),
                                   create_choice(
                                       name="orcana",
                                       value="orcana"
                                   ),
                                   create_choice(
                                       name="orcana+",
                                       value="orcana+"
                                   ),
                                   create_choice(
                                       name="orcana-",
                                       value="orcana-"
                                   )
                               ]
                           ),
                           create_option(
                               name="num_cards",
                               description="The dumber of cards to draw.",
                               option_type=4,
                               required=False
                           )
                       ])
    async def deck(self, ctx, cmd: str = 'standard', num_cards: int = 1):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {ctx.author} called DiceAndDeckCog.deck")
        global table
        try:
            table = card_deck.Deck(cmd.lower())
            if num_cards > 0:
                table.draw(num_cards)
            if num_cards > 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] \tnew \"{table}\" on table")
                print(f"[{datetime.now().strftime('%H:%M:%S')}] \t{ctx.author} drew {table.results(num_cards)}")
                await ctx.send(f"{ctx.author.display_name} created a new {table} and drew:\n"
                               f"{table.result(num_cards)}")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] \tnew \"{table}\" on table")
                await ctx.send(f"{ctx.author.display_name} created a new {table}.")
        except dice.DiceException as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] \terrored \"{e}\"")
            await ctx.send(f"**Error**: {e}")
        except Exception as e:
            traceback.print_exc()
            await ctx.send(f"**Error**: {e}")

    @cog_ext.cog_slash(name='draw',
                       description='Draws a card from the current deck.',
                       guild_ids=GUILD_IDS,
                       options=[
                           create_option(
                               name="num_cards",
                               description="The number of cards to draw. Defaults to 1",
                               option_type=4,
                               required=False
                           )
                       ])
    async def draw(self, ctx, num_cards: int = 1):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {ctx.author} called DiceAndDeckCog.draw")
        global table
        try:
            if type(table) is card_deck.Deck:
                if 0 < num_cards <= len(table):
                    table.draw(num_cards)
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] \t{ctx.author} drew {table.results(num_cards)} "
                          f"from the current {table}")
                    await ctx.send(f"{ctx.author.display_name}'s {table} card{'s are' if num_cards > 1 else ' is'}:\n"
                                   f"{table.results(num_cards)}")
                else:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] \terrored \"deck empty\"")
                    await ctx.send(f"**Error**: Not enough cards in deck\n"
                                   f"\tTry `/reshuffle`")
            elif type(table) is dice.Dice:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] \terrored \"no deck on table\"")
                await ctx.send(f"**Error**: Dice can't be drawn from\n"
                               f"\tTry `/reroll`")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] \terrored \"no deck on table\"")
                await ctx.send(f"**Error**: No current deck")
        except dice.DiceException as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] \terrored \"{e}\"")
            await ctx.send(f"**Error**: {e}")
        except Exception as e:
            traceback.print_exc()
            await ctx.send(f"**Error**: {e}")

    @cog_ext.cog_slash(name='reshuffle',
                       description='Restores the deck to its initial state',
                       guild_ids=GUILD_IDS)
    async def reshuffle(self, ctx):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {ctx.author} called DiceAndDeckCog.reshuffle")
        global table
        try:
            if type(table) is card_deck.Deck:
                table.reshuffle()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] \tdeck reshuffled")
                await ctx.send(f"{ctx.author.display_name} reshuffled the {table}")
            elif type(table) is dice.Dice:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] \terrored \"no deck on table\"")
                await ctx.send(f"**Error**: Dice can't be shuffled")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] \terrored \"no deck on table\"")
                await ctx.send(f"**Error**: No current deck")
        except dice.DiceException as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] \terrored \"{e}\"")
            await ctx.send(f"**Error**: {e}")
        except Exception as e:
            traceback.print_exc()
            await ctx.send(f"**Error**: {e}")


def setup(bot):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] dice_and_deck_cog initialised...")
    bot.add_cog(DiceAndDeckCog(bot))
