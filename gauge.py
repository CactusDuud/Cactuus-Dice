"""
Property of Sage L Mahmud (https://github.com/CactusDuud)
Intended to be implemented alongside main.py
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

from dice import Dice


class Gauge:
    def __init__(self, initial_max: int, recovery=None, fill=False):
        self.max = initial_max
        self.current = initial_max if fill else 0
        if recovery is None:
            self.recovery = None
        elif type(recovery) is int:
            self.recovery = recovery
        elif type(recovery) is str:
            Dice(recovery)
        else:
            raise TypeError(f"Gauge.recovery initialisation error ({type(recovery)})")

    def __str__(self):
        return f"{self.current}" \
               + (" " * (3 - len(str(self.current)))) \
               + ' / ' \
               + f"{self.max}" \
               + (" " * (3 - len(str(self.max))))

    def bar(self) -> str:
        """Returns a Unicode gauge"""
        ticks = int(((self.current / self.max) * 100) // 5)
        head = '[' if ticks >= 0 else ''
        bar_txt = '■' * ticks if ticks >= 0 else ''
        space_txt = ' ' * (20 - abs(ticks))
        antibar_txt = '□' * abs(ticks) if ticks < 0 else ''
        tail = ']' if ticks < 20 else ''
        return head + bar_txt + space_txt + antibar_txt + tail

    def ratio(self) -> float:
        """Returns the percent of the gauge filled"""
        return self.current / self.max

    def refresh(self, new_max=None, new_recovery=None, fill=False):
        """Refreshes gauge values"""
        self.max = self.max if None else new_max
        self.current = self.max if fill or self.max < self.current else self.current
        self.current = 0 if self.current < 0 else self.current
        self.recovery = self.recovery if None else new_recovery
