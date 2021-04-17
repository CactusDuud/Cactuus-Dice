"""
Property of Sage L Mahmud (https://github.com/CactusDuud)
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

from random import randint
import re


# https://regex101.com/r/r832Rb/1
ROLL_PATTERN = r'^' \
               r'(?P<rolls>[1-9][\d]*)?d(?P<faces>[1-9][\d]*)' \
               r'(?:(?P<modifier>e|r|h|k|l)(?P<modus>[1-9][\d]*)?)?' \
               r'(?:(?P<operator>[+\-*/%^])(?P<operand>[\d]+))?' \
               r'(?:(?P<comparison>[<>=!][=]?)(?P<comparator>[\d]+))?' \
               r'$'


class DiceException(Exception):
    pass


# Okay this should probably be a helper class but I don't think I'll make it one
class RollResults:
    def __init__(self, faces=None):
        self.faces = faces
        self.rolls = []
        self.dropped_indices = set()
        self.bonus_indices = set()

    def __iter__(self):
        return iter(self.rolls)

    def __str__(self):
        """Create roll sum portion (Ex: "(1 + 20)")"""
        addend_list = []
        for i in range(len(self.rolls)):
            pending_addend = self.rolls[i]

            # Drop striking
            if i in self.dropped_indices:
                pending_addend = f"~~{pending_addend}~~"

            # Bonus marking
            if i in self.bonus_indices:
                pending_addend = f"*{pending_addend}*"

            # Min/max highlighting
            if self.faces >= 3 and (self.rolls[i] == 1 or self.rolls[i] == self.faces):
                pending_addend = f"**{pending_addend}**"

            addend_list.append(str(pending_addend))

        return f"({' + '.join(addend_list)})"

    def add(self, new_roll: int, bonus=False) -> None:
        """Adds a roll to the list of roll results. Optionally marks a roll as a bonus roll."""
        self.rolls.append(new_roll)

        # Record bonus roll indices for later
        if bonus:
            self.bonus_indices.add(len(self.rolls)-1)

    def drop(self, dropped_index: int) -> None:
        """Marks the a roll to be dropped"""
        self.dropped_indices.add(dropped_index)

    def get_sum(self) -> int:
        """Returns the sum of the last roll as an int"""
        return sum([self.rolls[i] for i in range(len(self.rolls)) if i not in self.dropped_indices])


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
            self.print_result = ''
        else:
            raise DiceException("Invalid input parameters")

    def __str__(self):
        """Returns the die command used to generate these dice as a string"""
        return_str = f"{self.rolls if self.rolls > 1 else ''}d{self.faces}"
        return_str += f"{self.operator}{self.operand}" if self.operator is not None else ''
        return_str += f"{self.modifier}{self.modus}" if self.modifier is not None else ''
        # Temporarily removed, because it looks better
        # return_str += f"{self.comparison}{self.comparator}" if self.comparison is not None else ''
        return return_str

    def __len__(self):
        """returns the number of rolls"""
        return self.rolls

    def roll(self):
        """Rolls the dice"""
        # Clear cached values
        self.last_results = RollResults(self.faces)
        self.print_result = ''

        '''
        Valid modifiers:
            h : keeps modus highest dice (also takes k)
            l : keeps modus lowest dice
            e : rolls additional dice at the max number
            r : rerolls numbers equal or below modus
        '''

        # Keep x highest dice (keeps the x highest results)
        if self.modifier == 'h' or self.modifier == 'k':
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
            for _ in range(self.rolls):
                r = randint(1, self.faces)
                self.last_results.add(r)

                # Repeatedly roll again if max result
                loops = 1
                while r == self.faces and loops <= self.modus:
                    r = randint(1, self.faces)
                    self.last_results.add(r, bonus=True)
                    loops += 1

        # Rerolls numbers equal to or below x
        elif self.modifier == 'r':
            for i in range(self.rolls):
                r = randint(1, self.faces)
                self.last_results.add(r)

                if r <= self.modus:
                    self.last_results.drop(i-1)
                    self.last_results.add(randint(1, self.faces), bonus=True)

        # Standard case
        else:
            self.last_results.rolls = [randint(1, self.faces) for _ in range(self.rolls)]

    def operate(self, num: int) -> int:
        """Applies the stored operation on a number"""
        '''
        Valid operators:
            + : addition
            - : subtraction
            * : multiplication
            / : integer division
            % : modular division
            ^ : exponentiation
        '''

        if self.operator == '+':
            num += self.operand
        elif self.operator == '-':
            num -= self.operand
        elif self.operator == '*':
            num *= self.operand
        elif self.operator == '/':
            num //= self.operand
        elif self.operator == '%':
            num %= self.operand
        elif self.operator == '^':
            num **= self.operand

        return num

    def compare(self, num: int) -> str:
        """Returns a string following the boolean value of a number"""
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
            if num == self.comparator:
                return f' = {self.comparator} *(SUCCESS)*'
            else:
                return f' ≠ {self.comparator} *(FAILURE)*'

        elif self.comparison == '!' or self.comparison == '!=':
            if num != self.comparator:
                return f' ≠ {self.comparator} *(SUCCESS)*'
            else:
                return f' = {self.comparator} *(FAILURE)*'

        elif self.comparison == '<':
            if num < self.comparator:
                return f' < {self.comparator} *(SUCCESS)*'
            else:
                return f' ≥ {self.comparator} *(FAILURE)*'

        elif self.comparison == '>':
            if num > self.comparator:
                return f' > {self.comparator} *(SUCCESS)*'
            else:
                return f' ≤ {self.comparator} *(FAILURE)*'

        elif self.comparison == '<=':
            if num <= self.comparator:
                return f' ≤ {self.comparator} *(SUCCESS)*'
            else:
                return f' > {self.comparator} *(FAILURE)*'

        elif self.comparison == '>=':
            if num >= self.comparator:
                return f' ≥ {self.comparator} *(SUCCESS)*'
            else:
                return f' < {self.comparator} *(FAILURE)*'

    def results(self):
        """Return the results of the last roll"""

        if self.print_result == '':

            # Start with print version of the last roll, including drops and bonuses, as well as the sum
            # Ex: "(6 + 4 + 2)" with a sum of 12
            self.print_result = str(self.last_results)
            roll_sum = self.last_results.get_sum()

            # Calculate any operations
            # Ex: "(6 + 4 + 2) / 2" with a sum of 6
            if self.operator is not None:
                roll_sum = self.operate(roll_sum)
                self.print_result += f" {self.operator} {self.operand}"

            # Concatenate the final sum
            self.print_result += f" = {str(roll_sum)}"

            # Append comparisons
            if self.comparison is not None:
                self.print_result += self.compare(roll_sum)

        return self.print_result
