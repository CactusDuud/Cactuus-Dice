"""
Property of Sage L Mahmud (https://github.com/CactusDuud)
Hey! This is deprecated, but kept for archiving purposes. Don't use it :)
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

from random import randint
import re


def roll(commands: [str], verbose: bool = False) -> str:
    # Process standard command
    command = re.match(r'^(?P<rolls>[1-9][\d]*)?d(?P<faces>[1-9][\d]*)$', commands[0])
    rolls = int(command.group('rolls')) if command.group('rolls') is not None else 1
    roll_list = [randint(1, int(command.group('faces'))) for i in range(0, rolls)]

    # Process additional arguments
    for argument in commands[1:]:
        if re.match(r'^(?P<operator>[-+*/%^])(?P<value>[1-9][\d]*)$', argument) is not None:
            roll_list = operate(roll_list, re.match(r'^(?P<operator>[-+*/%^])(?P<value>[1-9][\d]*)$', argument))
        if re.match(r'^drop[\d]+$', argument) is not None:
            roll_list = drop(roll_list, re.match(r'^drop[\d]+$', argument))
        if re.match(r'^take[\d]+$', argument) is not None:
            roll_list = take(roll_list, re.match(r'^take[\d]+$', argument))

    # Construct return string
    return_str = f"{', '.join([str(i) for i in roll_list])}"
    if verbose:
        return_str = f"Summary:\n" \
            f"{sorted(roll_list)}\n" \
            f"Sum:\t{sum(roll_list)}\n" \
            f"Avg:\t{sum(roll_list) / len(roll_list)}"

    return return_str


def operate(roll_list: [int], argument) -> [int]:
    operator = argument.group('operator')
    value = int(argument.group('value'))
    if operator == '+':
        return [i + value for i in roll_list]
    elif operator == '-':
        return [i - value for i in roll_list]
    elif operator == '*':
        return [i * value for i in roll_list]
    elif operator == '/':
        return [i // value for i in roll_list]
    elif operator == '^':
        return [i ** value for i in roll_list]
    elif operator == '%':
        return [i % value for i in roll_list]


def drop(roll_list: [int], argument) -> [int]:
    new_rolls = [r for r in roll_list]
    value = int(argument.group(0)[4:])
    value = value if value < len(new_rolls) else len(new_rolls) - 1
    for i in range(0, value):
        new_rolls.remove(min(new_rolls))
    return new_rolls


def take(roll_list: [int], argument) -> [int]:
    roll_list_clone = [r for r in roll_list]
    new_rolls = []
    value = int(argument.group(0)[4:])
    value = value if value < len(roll_list_clone) else len(roll_list_clone)
    for i in range(0, value):
        new_rolls.append(max(roll_list_clone))
        roll_list_clone.remove(max(roll_list_clone))
    return new_rolls


if __name__ == '__main__':
    running = True
    while running:
        user_in = input('Enter command: ').lower().split()
        if user_in[0] == 'quit' or user_in[0] == 'q':
            running = False
        elif user_in[0] == 'roll' or user_in[0] == 'r':
            if re.match(r'^(?P<rolls>[1-9][\d]*)?d(?P<faces>[1-9][\d]*)$', user_in[1]) is not None:
                times = 1
                for argument in user_in[1:]:
                    if re.match(r'^(?P<value>[\d]+)times$', argument) is not None:
                        val = int(re.match(r'^(?P<value>[\d]+)times$', argument).group('value'))
                        times = val if val > times else 1
                for i in range(times):
                    print(roll(user_in[1:]) + '\n')
            elif user_in[1] == 'percent':
                print(f"{roll(['1d100'])}%" + '\n')
            elif user_in[1] == 'coin':
                print(('Heads!' if roll(['1d2', '%2']) == '1' else 'Tails!') + '\n')
            elif user_in[1] == 'die':
                print(roll(['1d6']) + '\n')
            elif re.match(r'^frac(?P<value>[\d]+)$', user_in[1]) is not None:
                percent = int(roll(['1d10000'])) / 10000
                frac_val = int(int(re.match(r'^frac(?P<value>[\d]+)$', user_in[1]).group('value')) * percent)
                print(f'{frac_val if frac_val > 1 else 1} ({percent * 100}%)' + '\n')
            else:
                print(f"Roll not recognised: {user_in[1]}")
        elif user_in[0] == 'roll+' or user_in[0] == 'r+':
            if re.match(r'^(?P<rolls>[1-9][\d]*)?d(?P<faces>[1-9][\d]*)$', user_in[1]) is not None:
                times = 1
                for argument in user_in[1:]:
                    if re.match(r'^(?P<value>[\d]+)times$', argument) is not None:
                        val = int(re.match(r'^(?P<value>[\d]+)times$', argument).group('value'))
                        times = val if val > times else 1
                for i in range(times):
                    print(roll(user_in[1:], True) + '\n')
            else:
                print(f"Roll not recognised: {user_in[1]}" + '\n')
        else:
            print(f"Command not recognised: {user_in[0]}" + '\n')
