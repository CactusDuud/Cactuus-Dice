"""
Property of Sage L Mahmud (https://github.com/CactusDuud)
Intended to be implemented alongside main.py
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

# Requirements:
#   dice addition and subtraction
#   count values
#   max
#   min
#   median
#   avg
#   sort

import dice
import fudge
import deck


class Hand:
    def __init__(self):
        self.contents = []

    def add(self, item):
        self.contents.append(item)
