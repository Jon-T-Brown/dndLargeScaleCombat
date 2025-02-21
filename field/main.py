import multiprocessing as mp
import json
from Unit import Unit
from random import randint
import os
from time import time


def timer(t_start, t_end, t_0=None):
    t_delta = t_end - t_start
    total = ""
    if t_0:
        t_delta_total = t_end - t_0
        total = f" (total {t_delta_total:.2f}s)"
    print(f"Took {t_delta:.2f}s{total}")


def load_army(filename):
    with open(filename, "r") as f:
        battalions = json.load(f)
    return [
        Unit(
            item["ac"],
            item["hp"],
            item["hit_bonus"],
            item["dmg_bonus"],
            item["dmg_dice"],
        )
        for item in battalions
        for _ in range(item["count"])
    ]


def get_attacks(army1, army2):
    army1len = len(army1) - 1
    army2len = len(army2) - 1
    return [(unit, army2[randint(0, army2len)]) for unit in army1] + [
        (unit, army1[randint(0, army1len)]) for unit in army2
    ]


def attack(attacker, target):
    if attacker.get_hp() > 0 and target.get_hp() > 0:
        if randint(1, 20) + attacker.get_hit_bonus() >= target.get_ac():
            target.dmg(randint(1, attacker.get_dmg_dice()) + attacker.get_dmg_bonus())


def resolve(army):
    return [unit for unit in army if unit.get_hp() > 0]


def player_kills(kills):
    for i in range(min(kills, len(army2)) - 1, -1, -1):
        army2.pop(i)


if __name__ == "__main__":
    t_init = time()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Load armies
    army1 = load_army("army1.json")
    army2 = load_army("army2.json")
    timer(t_init, time())

    with mp.Pool() as pool:
        while army1 and army2:
            t_turn_begin = time()
            print("Army 1:", len(army1))
            print("Army 2:", len(army2), "\n")

            player_kills = int(input("Input player kill total, then hit enter: "))
            army2 = army2[player_kills:]

            if not army2:
                break

            print("Processing attacks, please wait...")
            attacks = get_attacks(army1, army2)

            # Use starmap for better performance
            pool.starmap(attack, attacks)
            army1 = resolve(army1)
            army2 = resolve(army2)

            t_turn_end = time()
            timer(t_turn_begin, t_turn_end, t_init)

    print("War complete")
    print("Army 1:", len(army1))
    print("Army 2:", len(army2))
