class Unit:
    
    def __init__(self, ac, hp, hit_bonus, dmg_bonus, dmg_dice):
        self.ac = ac
        self.hp = hp
        self.hit_bonus=hit_bonus
        self.dmg_bonus=dmg_bonus
        self.dmg_dice=dmg_dice
    
    def get_ac(self):
        return self.ac
    
    def get_hp(self):
        return self.hp
    
    def dmg(self, dmg):
        self.hp -= dmg
    
    def get_hit_bonus(self):
        return self.hit_bonus
    
    def get_dmg_bonus(self):
        return self.dmg_bonus
    
    def get_dmg_dice(self):
        return self.dmg_dice
