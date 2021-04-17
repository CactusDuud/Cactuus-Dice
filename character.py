"""
Property of Sage L Mahmud (https://github.com/CactusDuud)
Intended to be implemented alongside main.py
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

from datetime import datetime
from dice import Dice
from gauge import Gauge
from random import randint


STAT_LIST = [
    'STR',
    'FRT',
    'CON',
    'INT',
    'WIS',
    'FOC',
    'DEX',
    'PER',
    'CHA'
]
RACE_INDEX = {
        'Human': {
            'Race': "Novian Human",
            'Roll': "3d6k2",
            'Roll Points': 18,
            'Bonuses': (0, 0, 0, 0, 0, 0, 0, 0, 0)
        },
        'Novianhuman': {
            'Race': "Novian Human",
            'Roll': "3d6k2",
            'Roll Points': 18,
            'Bonuses': (0, 0, 0, 0, 0, 0, 0, 0, 0)
        },
        'Vetusianhuman': {
            'Race': "Vetusian Human",
            'Roll': "3d6k2",
            'Roll Points': 18,
            'Bonuses': (0, 0, 0, 1, -1, 0, 0, 0, 0)
        },
        'Dwarf': {
            'Race': "Mountain Dwarf",
            'Roll': "3d6k2",
            'Roll Points': 18,
            'Bonuses': (0, 2, 0, -1, 1, 0, -2, 0, 0)
        },
        'Mountaindwarf':  {
            'Race': "Mountain Dwarf",
            'Roll': "3d6k2",
            'Roll Points': 18,
            'Bonuses': (0, 2, 0, -1, 1, 0, -2, 0, 0)
        },
        'Hilldwarf': {
            'Race': "Hill Dwarf",
            'Roll': "3d6k2",
            'Roll Points': 18,
            'Bonuses': (0, 2, 0, -1, 0, 0, -2, 1, 0)
        },
        'Deepsdwarf': {
            'Race': "Deeps Dwarf",
            'Roll': "3d6k2",
            'Roll Points': 18,
            'Bonuses': (0, 2, 0, -1, 1, 0, -2, 1, -1)
        },
        'Halfdwarf': {
            'Race': "Half-Dwarf",
            'Roll': "3d6k2",
            'Roll Points': 18,
            'Bonuses': (0, 1, 0, -1, 0, 0, -1, 0, 1)
        },
        'Dwelf': {
            'Race': "Dwelf",
            'Roll': "3d6k2",
            'Roll Points': 18,
            'Bonuses': (1, 0, 1, -1, 0, 0, 0, 0, -1)
        },
        'Elf': {
            'Race': "High Elf",
            'Roll': "3d6k2",
            'Roll Points': 18,
            'Bonuses': (0, -2, 1, 0, -1, 0, 2, 0, 0)
        },
        'Highelf': {
            'Race': "High Elf",
            'Roll': "3d6k2",
            'Roll Points': 18,
            'Bonuses': (0, -2, 1, 1, -1, 0, 2, 0, 0)
        },
        'Woodelf': {
            'Race': "Wood Elf",
            'Roll': "3d6k2",
            'Roll Points': 18,
            'Bonuses': (0, -2, 1, 0, -1, 0, 2, 1, 0)
        },
        'Seaelf': {
            'Race': "Sea Elf",
            'Roll': "3d6k2",
            'Roll Points': 18,
            'Bonuses': (0, -2, 1, 1, -2, 0, 2, 0, 1)
        },
        'Skyelf': {
            'Race': "Sky Elf",
            'Roll': "3d6k2",
            'Roll Points': 18,
            'Bonuses': (0, -3, 1, 1, -2, 0, 3, 0, 1)
        },
        'Sunelf': {
            'Race': "Sun Elf",
            'Roll': "3d6k2",
            'Roll Points': 18,
            'Bonuses': (0, -2, 2, 1, -2, 0, 2, 0, 0)
        },
        'Moonelf': {
            'Race': "Moon Elf",
            'Roll': "3d6k2",
            'Roll Points': 18,
            'Bonuses': (-1, -2, 1, 2, -1, 0, 2, 0, 0)
        },
        'Voidelf': {
            'Race': "Void Elf",
            'Roll': "3d6k2",
            'Roll Points': 18,
            'Bonuses': (0, -2, 1, 1, 0, 0, 2, 0, -1)
        },
        'Halfelf': {
            'Race': "Half-Elf",
            'Roll': "3d6k2",
            'Roll Points': 18,
            'Bonuses': (0, -1, -1, 0, 0, 0, 1, 1, 0)
        }
    }
PHI = (1 + 5 ** 0.5) / 2


class Attribute:
    def __init__(self, base: int, level: int = 1):
        self.base = base
        self.rate = randint(1, 20) / 100
        self.add_bonus = 0
        self.mul_bonus = 1.00

        self.score = int(self.base * self.mul_bonus + self.add_bonus)
        self.next = int(self.base + self.rate * (level + 1)) - int(self.base + self.rate * level)
        self.mod = (self.score - 10) // 2

    def __str__(self):
        return_str = f"(" if self.mul_bonus != 1.00 else f" "
        return_str += f"{self.score}" + (" " * (3 - len(str(self.score))))
        return_str += f" ×{self.mul_bonus})" if self.mul_bonus != 1.00 else f""
        return_str += f" +{self.add_bonus}" if self.add_bonus != 0 else f""
        return_str += f" [{sign(self.mod)}]"
        return return_str

    def __int__(self):
        return int(self.score)

    # TODO: Define comparisons

    def refresh(self, level: int = 1):
        """Recalculates derived values"""
        self.score = int(self.base * self.mul_bonus + self.add_bonus)
        self.next = int(self.base + self.rate * (level + 1)) - int(self.base + self.rate * level)
        self.mod = (self.score - 10) // 2

    def relative(self, other) -> str:
        """Determines the relative score as a str"""
        if self.score >= int(other) * 1.494:
            return "Superb"
        elif self.score >= int(other) * 1.433:
            return "Great"
        elif self.score >= int(other) * 1.191:
            return "Good"
        elif self.score >= int(other) * 0.809:
            return "Fair"
        elif self.score >= int(other) * 0.567:
            return "Mediocre"
        elif self.score >= int(other) * 0.506:
            return "Poor"
        elif self.score >= 0:
            return "Terrible"
        else:
            return "Unknown"

    def grow(self):
        """Increases the base stat by the rate"""
        self.base += self.rate


class Mood:
    def __init__(self):
        self.happiness = 0
        self.anticipation = 0
        self.trust = 0
        self.aggression = 0


class DeathSaves:
    def __init__(self):
        self.saves = 0
        self.fails = 0

    def __str__(self):
        return_str = 'O' * self.saves
        return_str += '-' * (6 - self.saves - self.fails)
        return_str += 'X' * self.fails
        return return_str

    def __bool__(self):
        return self.fails < 3


def calc_attributes(race) -> dict:
    return_dict = {
                'STR': None,
                'FRT': None,
                'CON': None,
                'INT': None,
                'WIS': None,
                'FOC': None,
                'DEX': None,
                'PER': None,
                'CHA': None
            }
    attr_die = Dice(RACE_INDEX[race]['Roll'])
    c = 0
    for k in return_dict:
        attr_die.roll()
        return_dict[k] = Attribute(attr_die.last_sum + RACE_INDEX[race]['Bonuses'][c])
        c += 1
    return return_dict


def calc_bst(attributes: dict, level: int) -> int:
    """:return total of all stats"""
    total = 0
    for attribute in attributes.values():
        total += int(attribute.base + attribute.rate * (level + 1))
    return total


def sign(val: int or float) -> str:
    """:return the string equivalent of the value with sign"""
    if type(val) is int:
        return f"+{val}" if val >= 0 else f"{val}"
    elif type(val) is float:
        return f"+{val:.2f}" if val >= 0 else f"{val:.2f}"
    else:
        try:
            return f"+{val}" if val >= 0 else f"{val}"
        except Exception:
            raise TypeError(f"Cannot return a signed {type(val)}")


class Character:
    def __init__(self, owner, cid, name: str, race: str):
        # Basic info
        self.owner = owner
        self.cid = cid
        self.aliases = [name]
        self.race = RACE_INDEX[race]['Race']
        self.race_key = race
        self.bg = None
        self.biography = None
        self.bday = None
        self.height = None
        self.weight = None
        self.appearance = None
        self.alive = DeathSaves()
        self.level = 1

        # Attributes
        self.attr_points = RACE_INDEX[race]['Roll Points']
        self.attributes = calc_attributes(race)
        self.bst = calc_bst(self.attributes, self.level)

        # Gauges
        self.xp = Gauge(int(self.level * PHI * 20))
        self.health = \
            Gauge(max((max(self.attributes['CON'].mod + 3, 1) * self.level + 9), 1),
                  f"1d6{'+' if self.attributes['CON'].mod >= 0 else ''}{self.attributes['CON'].mod}",
                  True)
        self.aura = \
            Gauge(max((max(self.attributes['FOC'].mod + 2, 1) * self.level + 6), 1),
                  f"1d4{'+' if self.attributes['FOC'].mod >= 0 else ''}{self.attributes['FOC'].mod}",
                  True)
        self.stamina = \
            Gauge(max((self.attributes['FRT'].mod * 10 + 100), 10),
                  f"2d20{'+' if self.attributes['CHA'].mod >= 0 else ''}{self.attributes['CHA'].mod}",
                  True)
        self.fullness = \
            Gauge(max((self.attributes['CON'].mod * 10 + 100), 10),
                  fill=True)
        self.hydration = \
            Gauge(max((self.attributes['CON'].mod * 10 + 100), 10),
                  fill=True)
        self.immunity = \
            Gauge(max((self.attributes['CON'].mod * 10 + 100), 10),
                  f"1d10{'+' if self.attributes['CON'].mod >= 0 else ''}{self.attributes['CON'].mod}",
                  True)
        self.morale = \
            Gauge(max((self.attributes['FOC'].mod * 10 + 100), 10),
                  f"1d20{'+' if self.attributes['CHA'].mod >= 0 else ''}{self.attributes['CHA'].mod}",
                  True)
        self.sanity = \
            Gauge(max((self.attributes['FOC'].mod * 10 + 100), 10),
                  f"1d20{'+' if self.attributes['CHA'].mod >= 0 else ''}{self.attributes['CHA'].mod}",
                  True)

        # Derived stats
        self.age = None
        self.carry_weight = Gauge(self.attributes['FRT'] * 2.5)
        self.move_speed = int(max((self.attributes['DEX'] // 5) * (1.0 - self.carry_weight.ratio()), 0))
        self.initiative = (self.attributes['DEX'] + self.attributes['PER']) // 2
        self.action_points = Gauge(6 + self.initiative, 6 + self.initiative, True)

        # Equipment stats TODO: Implement inventory, equipment, and etc.
        self.inventory = []

        # Miscellaneous TODO: Mood, stance, status effects, skills, and traits
        self.mood = Mood()
        self.stance = None
        self.status_effects = []
        self.skills = []
        self.traits = []

    def refresh(self, time: datetime = None, fill: bool = False):
        """Recalculates derived information after an update"""
        # Update stats
        for a in self.attributes:
            self.attributes[a].refresh(self.level)
        self.bst = calc_bst(self.attributes, self.level)

        # Health gauges
        self.health.refresh(
            new_max=max((self.attributes['CON'].mod * (self.level // 4) + 12), 1),
            new_recovery=f"1d6{'+' if self.attributes['CON'].mod >= 0 else ''}{self.attributes['CON'].mod}",
            fill=fill
        )
        self.aura.refresh(
            new_max=max((self.attributes['FOC'].mod * (self.level // 8) + 8), 1),
            new_recovery=f"1d4{'+' if self.attributes['FOC'].mod >= 0 else ''}{self.attributes['FOC'].mod}",
            fill=fill
        )
        self.stamina.refresh(
            new_max=max((self.attributes['FRT'].mod * 10 + 100), 10),
            new_recovery=f"2d20{'+' if self.attributes['CHA'].mod >= 0 else ''}{self.attributes['CHA'].mod}",
            fill=fill
        )
        self.fullness.refresh(new_max=max((self.attributes['CON'].mod * 10 + 100), 10), fill=fill)
        self.hydration.refresh(new_max=max((self.attributes['CON'].mod * 10 + 100), 10), fill=fill)
        self.immunity.refresh(
            new_max=max((self.attributes['CON'].mod * 10 + 100), 10),
            new_recovery=f"1d10{'+' if self.attributes['CON'].mod >= 0 else ''}{self.attributes['CON'].mod}",
            fill=fill
        )
        self.morale.refresh(
            new_max=max((self.attributes['FOC'].mod * 10 + 100), 10),
            new_recovery=f"1d20{'+' if self.attributes['CHA'].mod >= 0 else ''}{self.attributes['CHA'].mod}",
            fill=fill
        )
        self.sanity.refresh(
            new_max=max((self.attributes['FOC'].mod * 10 + 100), 10),
            new_recovery=f"1d20{'+' if self.attributes['CHA'].mod >= 0 else ''}{self.attributes['CHA'].mod}",
            fill=fill
        )

        # Derived stats
        self.age = None if self.age is None or time is None else (time - self.age).years
        self.carry_weight.refresh(new_max=self.attributes['FRT'] * 2.5)
        self.move_speed = int(max((self.attributes['DEX'] // 5) * (1.0 - self.carry_weight.ratio()), 0))
        self.initiative = (self.attributes['DEX'] + self.attributes['PER']) // 2
        self.action_points.refresh(new_max=6 + self.initiative, new_recovery=6 + self.initiative, fill=fill)

    def assign(self, p_attr: [int]) -> bool:
        """:return boolean based on the success of point assignment"""
        point_total = 0
        for i in range(9):
            if p_attr[i] - self.attributes[STAT_LIST[i]].base < 0:
                return False
            elif p_attr[i] - self.attributes[STAT_LIST[i]].base == 0:
                pass
            elif p_attr[i] <= 8:
                point_total += p_attr[i] - self.attributes[STAT_LIST[i]].base
            elif p_attr[i] <= 12:
                if self.attributes[STAT_LIST[i]].base > 8:
                    point_total += 2 * (p_attr[i] - self.attributes[STAT_LIST[i]].base)
                else:
                    point_total += 8 - self.attributes[STAT_LIST[i]].base
                    point_total += 2 * (p_attr[i] - 8)
            elif p_attr[i] <= 15 + RACE_INDEX[self.race_key]['Bonuses'][i]:
                if self.attributes[STAT_LIST[i]].base > 8:
                    if self.attributes[STAT_LIST[i]].base > 12:
                        point_total += 3 * (p_attr[i] - self.attributes[STAT_LIST[i]].base)
                    else:
                        point_total += 2 * (12 - self.attributes[STAT_LIST[i]].base)
                        point_total += 3 * (p_attr[i] - 12)
                else:
                    point_total += 8 - self.attributes[STAT_LIST[i]].base
                    point_total += 2 * (12 - 8)
                    point_total += 3 * (p_attr[i] - 12)
            else:
                return False

        if point_total <= self.attr_points:
            for i in range(9):
                self.attributes[STAT_LIST[i]].base = p_attr[i]
            self.attr_points -= point_total
            self.refresh()
            return True

        return False

    def gain_xp(self, dice_str: str) -> str:
        """
        Increases the user's total experience
        :return text containing the results
        """
        # TODO: Tie in skills and y'know, actually write this
        old_level = self.level

        gain = Dice(dice_str).roll()
        gain = gain.last_sum
        self.xp.current += gain
        while self.xp.current >= self.xp.max:
            self.level += 1
            for attr in self.attributes.values():
                attr.grow()
            self.xp.current -= self.xp.max

        return_str = f"{self.aliases[0]} gained {gain} xp!\n"
        return_str += f"{self.aliases[0]} levelled up!\n" if self.level > old_level else ''

        return return_str

    def info(self, mode='all') -> str:
        """:return detailed information on the character as a string"""
        alias_info = True if mode in ('all', 'bio') else False
        bio_info = True if mode in ('all', 'bio') else False
        status_info = True if mode in ('all', 'status') else False
        attribute_info = True if mode in ('all', 'attributes', 'bio') else False
        attribute_detail = True if mode in ('all', 'attributes') else False

        # Name info
        return_str = f"**{self.aliases[0]}** (CID:{self.cid} - owned by <@{self.owner}>)\n"
        return_str += f"\taka {', '.join(self.aliases[1:])}\n" if len(self.aliases) > 1 and alias_info else ''

        # Bio info
        return_str += f"Lvl.{self.level} ({self.xp} - {(self.xp.ratio() * 100):.2f}%) {self.bg} {self.race}\n"
        if bio_info:
            return_str += f"{self.age} years old - " if self.age is not None else f"Unknown age - "
            return_str += f"{self.height:.2f}m - " if self.height is not None else f"Unknown height - "
            return_str += f"{self.weight:.2f}kg\n" if self.weight is not None else f"Unknown weight\n"
            return_str += f"{self.appearance}\n" if self.appearance is not None else ''
            return_str += f"__Biography:__ {self.biography}\n" if self.biography is not None else ''
            return_str += '\n'

        # Status info
        if status_info:
            return_str += f"__Health:__\n"
            return_str += '```'
            return_str += f"HP: {self.health} ({(self.health.ratio() * 100):.2f}%)\n"
            return_str += f"AP: {self.aura} ({(self.aura.ratio() * 100):.2f}%)\n"
            return_str += f"Saves: {str(self.alive)}\n"
            return_str += '\n'
            return_str += f"Stamina  : {self.stamina} ({(self.stamina.ratio() * 100):.2f}%)\n"
            return_str += f"Fullness : {self.fullness} ({(self.fullness.ratio() * 100):.2f}%)\n"
            return_str += f"Hydration: {self.hydration} ({(self.hydration.ratio() * 100):.2f}%)\n"
            return_str += f"Immunity : {self.immunity} ({(self.immunity.ratio() * 100):.2f}%)\n"
            return_str += f"Morale   : {self.morale} ({(self.morale.ratio() * 100):.2f}%)\n"
            return_str += f"Sanity   : {self.sanity} ({(self.sanity.ratio() * 100):.2f}%)\n"
            return_str += '```'
            return_str += '\n'  # TODO: Add statuses, mood, stance

        # Attribute info
        if attribute_info:
            return_str += f"__Attributes:__\n"
            return_str += '```'
            return_str += f"Strength    : {self.attributes['STR']}"
            if attribute_detail and self.attributes['STR'].next != 0:
                return_str += f" next> {sign(self.attributes['STR'].next)}\n"
            else:
                return_str += "\n"
            return_str += f"Fortitude   : {self.attributes['FRT']}"
            if attribute_detail and self.attributes['FRT'].next != 0:
                return_str += f" next> {sign(self.attributes['FRT'].next)}\n"
            else:
                return_str += "\n"
            return_str += f"Constitution: {self.attributes['CON']}"
            if attribute_detail and self.attributes['CON'].next != 0:
                return_str += f" next> {sign(self.attributes['CON'].next)}\n"
            else:
                return_str += "\n"
            return_str += f"Intelligence: {self.attributes['INT']}"
            if attribute_detail and self.attributes['INT'].next != 0:
                return_str += f" next> {sign(self.attributes['INT'].next)}\n"
            else:
                return_str += "\n"
            return_str += f"Wisdom      : {self.attributes['WIS']}"
            if attribute_detail and self.attributes['WIS'].next != 0:
                return_str += f" next> {sign(self.attributes['WIS'].next)}\n"
            else:
                return_str += "\n"
            return_str += f"Focus       : {self.attributes['FOC']}"
            if attribute_detail and self.attributes['FOC'].next != 0:
                return_str += f" next> {sign(self.attributes['FOC'].next)}\n"
            else:
                return_str += "\n"
            return_str += f"Dexterity   : {self.attributes['DEX']}"
            if attribute_detail and self.attributes['DEX'].next != 0:
                return_str += f" next> {sign(self.attributes['DEX'].next)}\n"
            else:
                return_str += "\n"
            return_str += f"Perception  : {self.attributes['PER']}"
            if attribute_detail and self.attributes['PER'].next != 0:
                return_str += f" next> {sign(self.attributes['PER'].next)}\n"
            else:
                return_str += "\n"
            return_str += f"Charisma    : {self.attributes['CHA']}"
            if attribute_detail and self.attributes['CHA'].next != 0:
                return_str += f" next> {sign(self.attributes['CHA'].next)}\n"
            else:
                return_str += "\n"
            return_str += f"\n{self.bst} total ({self.bst / 9:.2f} average)" if attribute_detail else ''
            return_str += '```'
            return_str += '\n'

        # Move speed and initiative

        # Carry and equipment and/or inventory

        # Feats (Traits and skills)

        return return_str

    def observe(self, observer, mode='all') -> str:
        """:return obscured info on the character as a string"""
        bio_info = True if mode in ('all', 'bio') else False
        status_info = True if mode in ('all', 'status') else False
        attribute_info = True if mode in ('all', 'attributes', 'bio') else False

        # Name info
        return_str = f"**{self.aliases[0]}**\n"

        # Bio info
        return_str += f"Lvl.{self.level // 20 * 20} {self.race}\n"
        if bio_info:
            return_str += f"{self.age // 10 * 10} years old - " if self.age is not None else f"Unknown age - "
            return_str += f"{self.height // 10 * 10}m - " if self.height is not None else f"Unknown height - "
            return_str += f"{self.weight // 10 * 10}kg\n" if self.weight is not None else f"Unknown weight\n"
            return_str += f"{self.appearance}\n" if self.appearance is not None else ''
            return_str += '\n'

        # Status info
        if status_info:
            return_str += f"HP: {self.health.bar()}\n"
            return_str += '\n'  # TODO: Add statuses, mood, stance

        # Attribute info
        if attribute_info:
            return_str += f"__Attributes:__\n"
            return_str += '```'
            return_str += f"Strength    : {self.attributes['STR'].relative(observer.attributes['STR'])}\n"
            return_str += f"Fortitude   : {self.attributes['FRT'].relative(observer.attributes['FRT'])}\n"
            return_str += f"Constitution: {self.attributes['CON'].relative(observer.attributes['CON'])}\n"
            return_str += f"Intelligence: {self.attributes['INT'].relative(observer.attributes['INT'])}\n"
            return_str += f"Wisdom      : {self.attributes['WIS'].relative(observer.attributes['WIS'])}\n"
            return_str += f"Focus       : {self.attributes['FOC'].relative(observer.attributes['FOC'])}\n"
            return_str += f"Dexterity   : {self.attributes['DEX'].relative(observer.attributes['DEX'])}\n"
            return_str += f"Perception  : {self.attributes['PER'].relative(observer.attributes['PER'])}\n"
            return_str += f"Charisma    : {self.attributes['CHA'].relative(observer.attributes['CHA'])}\n"
            return_str += '```'
            return_str += '\n'

        # Equipment

        return return_str
