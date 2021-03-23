"""
Property of Sage L Mahmud (https://github.com/CactusDuud)
Intended to be implemented alongside discord_dice.py
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

from random import randint
import re


# https://regex101.com/r/lY0AAN/1
ROLL_PATTERN = r'^' \
               r'(?P<rolls>[1-9][\d]*)?d(?P<faces>[1-9][\d]*)' \
               r'(?:(?P<modifier>e|r|h|l)(?P<modus>[1-9][\d]*)?)?' \
               r'(?:(?P<operator>[+\-*/%^])(?P<operand>[\d]+))?' \
               r'(?:(?P<comparison>[<>=!][=]?)(?P<comparator>[\d]+))?' \
               r'$'


class DiceException(Exception):
    pass


class RollResults:
    def __init__(self):
        self.rolls = []
        self.dropped = set()
        self.bonus = set()
        self.sum = None

    def __iter__(self):
        return iter(self.rolls)

    def add(self, new_roll, bonus=False):
        """Adds a roll to the list of roll results"""
        self.rolls.append(new_roll)
        self.sum = new_roll if self.sum is None else self.sum + new_roll

        # Record bonus rolls
        if bonus:
            self.bonus.add(new_roll)

    def drop(self, dropped_index):
        """Marks a result of the roll to be dropped, updating the sum"""
        self.dropped.add(dropped_index)
        self.sum -= self.rolls[dropped_index]


class Dice:
    def __init__(self, cmd: str):
        self.match = re.match(ROLL_PATTERN, cmd)
        if self.match is not None:
            # The number of rolls (default 1) and faces of the die
            self.rolls = int(self.match.group('rolls')) if self.match.group('rolls') is not None else 1
            self.faces = int(self.match.group('faces'))

            # The optional modifier of the die and doubly optional modus (default 1)
            self.modifier = self.match.group('modifier')
            self.modus = int(self.match.group('modus')) if self.match.group('modus') is not None else 1

            # The optional operator of the die and operand (default 1, yay identities!)
            self.operator = self.match.group('operator')
            self.operand = int(self.match.group('operand')) if self.match.group('operand') is not None else 1

            # The optional comparison of the die and comparator (default 0)
            self.comparison = self.match.group('comparison')
            self.comparator = int(self.match.group('comparator')) if self.match.group('comparator') is not None else 0

            # Cached results for later reference
            self.last_results = RollResults()
            self.print_results = ''
            self.print_sum = ''
        else:
            raise DiceException("Invalid input parameters")

    def __str__(self):
        """Returns the die command used to generate these dice as a string"""
        return_str = f"{self.rolls if self.rolls > 1 else ''}d{self.faces}"
        return_str += f"{self.operator}{self.operand}" if self.operator is not None else ''
        return_str += f"{self.modifier}{self.modus}" if self.modifier is not None else ''
        return_str += f" {self.comparison}{self.comparator}" if self.comparison is not None else ''
        return return_str

    def __len__(self):
        """returns the number of rolls"""
        return self.rolls

    def roll(self):
        """Rolls the dice"""
        # Re-initialise values
        self.last_results = RollResults()
        self.print_results = ''
        self.print_sum = ''

        '''
        Valid modifiers:
            h : keeps modus highest dice
            l : keeps modus lowest dice
            e : rolls additional dice at the max number
            r : rerolls numbers equal or below modus
        '''

        # Keep x highest dice (keeps the x highest results)
        if self.modifier == 'h':
            self.last_results.rolls = [randint(1, self.faces) for _ in range(self.rolls)]

            # Remove ascending values from an enumerated list
            keep = sorted(list(enumerate([_ for _ in self.last_results])), key=lambda x: x[1])
            for _ in range(self.rolls - self.modus):
                self.last_results.drop(keep[0][0])
                keep.remove(keep[0])

        # Keep x lowest case (keeps the x lowest results)
        elif self.modifier == 'l':
            self.last_results.rolls = [randint(1, self.faces) for _ in range(self.rolls)]

            # Remove descending values from an enumerated list
            keep = sorted(list(enumerate([_ for _ in self.last_results])), key=lambda x: x[1], reverse=True)
            for _ in range(self.rolls - self.modus):
                self.last_results.drop(keep[0][0])
                keep.remove(keep[0])

        # Explode x times case (rolls again on max result up to x times)
        elif self.modifier == 'e':
            for i in range(self.rolls):
                r = randint(1, self.faces)
                self.last_results.add(r)

                # Repeatedly roll again if max result
                loops = 0
                while r == self.faces and loops <= self.modus:
                    r = randint(1, self.faces)
                    if r == self.faces:
                        self.last_results.add(r, bonus=True)
                    loops += 1

        # Rerolls numbers equal to or below x
        elif self.modifier == 'r':
            bonus = 1
            for i in range(self.rolls):
                r = randint(1, self.faces)
                self.last_results += [r]
                if r <= self.modus:
                    self.last_results += [randint(1, self.faces)]
                    self.dropped_results.add(i + bonus - 1)
                    self.bonus_results.add(i + bonus)
                    bonus += 1

        # Standard case
        else:
            self.last_results = [randint(1, self.faces) for _ in range(self.rolls)]

        # Calculate sum of rolls
        self.count_sum()

    def count_sum(self):
        """Updates the sum of the last roll results"""

        for i in range(len(self.last_results)):
            if i not in self.dropped_results:
                self.last_sum += self.last_results[i]

        # Modify sum based on operator
        if self.operator == '+':
            self.last_sum += self.operand
        elif self.operator == '-':
            self.last_sum -= self.operand
        elif self.operator == '*':
            self.last_sum *= self.operand
        elif self.operator == '/':
            self.last_sum //= self.operand
        elif self.operator == '%':
            self.last_sum %= self.operand
        elif self.operator == '^':
            self.last_sum **= self.operand

        self.last_sum = 1 if self.last_sum < 1 else self.last_sum

    def results(self) -> str:
        """Returns the results of the last roll as a string"""
        if self.print_results == '':

            # Create roll sum portion (Ex: "(1 + 20)")
            print_list = []
            for i in range(len(self.last_results)):

                # Min/Max highlighting and drop striking
                if i in self.dropped_results:
                    print_list += [f"~~{self.last_results[i]}~~"]
                elif i in self.bonus_results:
                    print_list += [f"*{self.last_results[i]}*"]
                elif self.faces >= 3 \
                        and (self.last_results[i] == 1 or self.last_results[i] == self.faces):
                    print_list += [f"**{self.last_results[i]}**"]
                else:
                    print_list += [str(self.last_results[i])]
            self.print_results = f"({' + '.join(print_list)})"

            # Append the operator
            if self.operator is not None:
                self.print_results += f" {self.operator} {self.operand}"

        return self.print_results

    def sum(self) -> str:
        """Returns the sum of the last roll as a string"""

        if self.print_sum == '':
            self.print_sum = str(self.last_sum)

            # Format fail/success based on comparison
            '''
            Valid comparisons:
                = : equal to (also ==)
                ! : not equal to (also !=)
                > : greater than
                < : less than
                > : greater than or equal to
                < : less than or equal to
            '''
            if self.comparison == '=' or self.comparison == '==':
                if self.last_sum == self.comparator:
                    self.print_sum += f' = {self.comparator} **SUCCESS**'
                else:
                    self.print_sum += f' ≠ {self.comparator} **FAILURE**'
            elif self.comparison == '!' or self.comparison == '!=':
                if self.last_sum != self.comparator:
                    self.print_sum += f' ≠ {self.comparator} **SUCCESS**'
                else:
                    self.print_sum += f' = {self.comparator} **FAILURE**'
            elif self.comparison == '<':
                if self.last_sum < self.comparator:
                    self.print_sum += f' < {self.comparator} **SUCCESS**'
                else:
                    self.print_sum += f' ≥ {self.comparator} **FAILURE**'
            elif self.comparison == '>':
                if self.last_sum > self.comparator:
                    self.print_sum += f' > {self.comparator} **SUCCESS**'
                else:
                    self.print_sum += f' ≤ {self.comparator} **FAILURE**'
            elif self.comparison == '<=':
                if self.last_sum <= self.comparator:
                    self.print_sum += f' ≤ {self.comparator} **SUCCESS**'
                else:
                    self.print_sum += f' > {self.comparator} **FAILURE**'
            elif self.comparison == '>=':
                if self.last_sum >= self.comparator:
                    self.print_sum += f' ≥ {self.comparator} **SUCCESS**'
                else:
                    self.print_sum += f' < {self.comparator} **FAILURE**'

        return self.print_sum
