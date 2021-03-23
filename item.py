"""
Property of Sage L Mahmud (https://github.com/CactusDuud)
Intended to be implemented alongside discord_dice.py
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

from gauge import Gauge

'''
Valid equip slots:
Head
Neck
Torso
Back
Arms
Hands
Waist
Legs
Feet
Accessory1
Accessory2
'''


class Item:
    def __int__(self, name, durability):
        self.name = name
        self.durability = Gauge(durability, fill=True)
