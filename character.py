"""
Property of Sage L Mahmud (https://github.com/CactusDuud)
Intended to be implemented alongside main.py
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

from datetime import date, timedelta
from dice import Dice


class CharacterException(Exception):
    pass


class Attribute:
    # TODO: Decide how buffs are calculated
    def __init__(self, name: str, proficiencies: dict[str, int]):
        self.value = 0
        self.name = name
        self.proficiencies = proficiencies

    def __str__(self):
        return f"{self.name} [{self.value / 10:+}]"

    def __int__(self):
        return self.value

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return other + self.value

    def __getitem__(self, item):
        return self.value + self.proficiencies[item]

    def set(self, value: int, proficiency: str = ''):
        if proficiency != '':
            try:
                self.proficiencies[proficiency] = value
            except KeyError:
                raise CharacterException(f"Proficiency {proficiency} does not exist")
        else:
            self.value = value


class Character:
    def __init__(self, ancestry: str, character_name: str, player):
        class Gauge:
            def __init__(self, base: int, stat: str):
                self.max = base + self.attributes[stat]
                self.value = base + self.attributes[stat]

            def __add__(self, other):
                return self.value + other

            def __radd__(self, other):
                return other + self.value

            def __iadd__(self, other):
                self.value += other
                if self.value > self.max:
                    self.value = self.max

            def __str__(self):
                pass

            def overflow(self, value):
                self.value += value

        # TODO: Check for valid ancestry and factor into character creation
        self.ancestry = ancestry
        self.character_name = character_name
        self.player = player

        # TODO: Allow users to set these traits
        self.aliases = [self.character_name]
        self.dob = date(0, 1, 1)
        self.base_height = 0
        self.base_weight = 0
        self.appearance = ""
        self.background = ""

        # TODO: Allow users to set attributes
        self.attributes = {
            "AGI": Attribute("Agility", {
                "Acrobatics": 0,
                "Finesse": 0,
                "Reflexes": 0,
                "Stealth": 0
            }),
            "CHM": Attribute("Charm", {
                "Performance": 0,
                "Persuasion": 0
            }),
            "FRT": Attribute("Fortitude", {
                "Athletics": 0,
                "Combat": 0,
                "Core": 0,
                "Grip": 0
            }),
            "GUT": Attribute("Guts", {
                "Consciousness": 0,
                "Digestion": 0,
                "Endurance": 0,
                "Immunity": 0
            }),
            "KEN": Attribute("Keenness", {
                "Accuracy": 0,
                "Insight": 0,
                "Instinct": 0,
                "Investigation": 0,
                "Perception": 0
            }),
            "SAG": Attribute("Sagacity", {
                "Crafts": 0,
                "Cuisine": 0,
                "Mechanics": 0,
                "Religion": 0,
                "Society": 0
            }),
            "WIT": Attribute("Wit", {
                "Arcana": 0,
                "Geography": 0,
                "History": 0,
                "Logic": 0,
                "Medicine": 0,
                "Nature": 0
            })
        }

        self.traits = []

        # Gauges
        self.health = Gauge(80)
        self.sanity = Gauge(80 + self.attributes["SAG"])
        self.stamina = Gauge(80 + self.attributes["GUT"])
        self.luck = Gauge(Dice("3d6").roll())
        self.xp = Gauge(0)

    def total_weight(self):
        # TODO: Add carried weight
        return self.base_weight

    def size(self):
        return (self.base_height * self.total_weight()) // 2

    def carry_weight(self):
        return round((self.size() / 4) * (100 + self.attributes["FRT"]["Core"]) / 100, 3)

    def movement(self, mode: str = 'Walk'):
        if mode == 'Walk':
            return self.base_height * 0.83 * 100 + self.attributes["AGI"]["Acrobatics"] / 100
        if mode == 'Sprint':
            return 1.5 * self.base_height * 0.83 * 100 + self.attributes["AGI"]["Acrobatics"] / 100
        if mode == 'Crawl':
            return 0.5 * self.base_height * 0.83 * 100 + self.attributes["AGI"]["Acrobatics"] / 100
        if mode == 'Climb':
            return 0.167 * self.base_height * 0.83 * 100 + self.attributes["FRT"]["Grip"] / 100
        if mode == 'Swim':
            return 0.167 * self.base_height * 0.83 * 100 + self.attributes["FRT"]["Athletics"] / 100
        if mode == 'Fly':
            return 0
        else:
            raise CharacterException(f"Movement type {mode} does not exist")

    def initiative(self):
        return self.attributes[""]

    def reach(self):
        # TODO: Factor in tools
        return round((self.base_height * 0.34) / 100, 3)

    def age(self, other_time: date) -> timedelta:
        return other_time - self.dob

    def add_alias(self, new_alias):
        self.aliases.append(new_alias)

    def get_ap(self):
        return 6 + (int(self.attributes["AGI"]) // 20)



"""
class Character:
    def __init__(self, occupation: str, ancestry: str, character_name: str, owner):
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
        # Recalculates derived information after an update
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
        # return boolean based on the success of point assignment
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
        # Increases the user's total experience :return text containing the results
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
        # return detailed information on the character as a string
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
        # return obscured info on the character as a string
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
"""
