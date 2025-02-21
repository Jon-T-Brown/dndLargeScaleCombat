import multiprocessing as mp
import json
from Unit import Unit
from random import shuffle, randint
import os
from multiprocessing.managers import SyncManager

class MyManager(SyncManager):
    pass

def get_army1(manager):
    with open("army1.json", "r") as f:
        battalions = json.load(f)
        for item in battalions:
            for i in range(0, item["count"]):
                army1.append(manager.Unit(item["ac"], item["hp"], item["hit_bonus"], item["dmg_bonus"], item["dmg_dice"]))
                
def get_army2(manager):
    with open("army2.json", "r") as f:
        battalions = json.load(f)
        for item in battalions:
            for i in range(0, item["count"]):
                army2.append(manager.Unit(item["ac"], item["hp"], item["hit_bonus"], item["dmg_bonus"], item["dmg_dice"]))
                
def get_attacks(attacks):
    army1len = len(army1)-1
    army2len = len(army2)-1
    for unit in army1:
        attacks.append((unit, army2[randint(0,army2len)]))
    for unit in army2:
        attacks.append((unit, army1[randint(0,army1len)]))
    shuffle(attacks)
    
def attack(attack):
    attacker = attack[0]
    target = attack[1]
    if (attacker.get_hp() > 0 and target.get_hp() > 0):
        if (randint(1,20)+attacker.get_hit_bonus() >= target.get_ac()):
            target.dmg(randint(1,attacker.get_dmg_dice())+attacker.get_dmg_bonus())

def resolve():
    for i in range(len(army1)-1,-1,-1):
        if (army1[i].get_hp() <= 0):
            army1.pop(i)
    for i in range(len(army2)-1,-1,-1):
        if (army2[i].get_hp() <= 0):
            army2.pop(i)    
            
def player_kills(kills):
    for i in range(min(kills,len(army2))-1,-1,-1):
        army2.pop(i)     

MyManager.register('Unit', Unit)

if __name__ == '__main__':
    with MyManager() as manager:
        army1 = manager.list()
        army2 = manager.list()
        attacks = manager.list()
        os.chdir("c:\\Git Projects\\dndCombat\\field")
        get_army1(manager)
        get_army2(manager)


        while (len(army1) > 0 and len(army2) > 0):
            print("Army 1:",len(army1))
            print("Army 2:",len(army2),"\n")
            player_kills(int(input("Input player kill total, then hit enter: ")))
            print("This may take a moment")
            resolve()
            attacks = []
            get_attacks(attacks)
            with mp.Pool() as pool:
                pool.map(attack, attacks)
            resolve()
            
        print("Army 1: ",len(army1))
        print("Army 2: ",len(army2),"\n")