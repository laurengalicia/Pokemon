import random
import Types as t

class Move():
    name = ''
    def __init__(self, name, power, defender=[0,0], attacker=0):
        self.name     = name
        self.power    = power
        self.defender = defender
        self.attacker = attacker
    def use(self, attacker, defender):
        level_factor = 2 + attacker.lvl() * 2/5
        power = self.power / (2 if attacker.burned else 1)
        print(attacker.attack, '/', defender.defense)
        print(f"2 + {level_factor} * {power} * {attacker.attack/defender.defense/50}")
        base_damage = 2 + level_factor * power * attacker.attack/defender.defense/50
        effect = 1
        for key in self.effective.keys():
            for type in defender.type:
                if type in self.effective[key]:
                    effect *= key
        same_type_bonus = 1.5 if self.type == attacker.type else 1
        random_factor = random.randrange(85, 100)/100
        modified_damage = base_damage * effect * same_type_bonus * random_factor
        print(f"{base_damage} * {effect} * {same_type_bonus} * {random_factor}")
        print(modified_damage)
        defender.HP -= int(modified_damage)
        attacker.HP  = int(attacker.HP - attacker.HP * attacker.poisoned + attacker.burned)
        result = []
        if attacker.paralyzed > 0 and random.randrange(100) < 25:
            result = [f"-->{attacker.name} is fully paralyzed!"]
        else:
            if effect >= 1.5:
                result = ["-->It's super effective!"]
            if self.defender[0] > 0:
                defender.attack -= self.defender[0]
                result = [f"-->{defender.name}'s attack fell!"]
            if self.defender[1] > 0:
                defender.defense -= self.defender[1]
                result = [f"-->{defender.name}'s defense fell!"]
            if self.attacker > 0:
                attacker.defense += self.attacker
                result = [f"-->{attacker.name}'s defense rose!"]
        attacker.attack = attacker.base_attack
        return result

class Normal(Move):
    type = t.normal
    effective = {  0:[],
                  .5:[t.rock, t.ghost, t.steel],
                 1.5:[]
                }

class Water(Move):
    type = t.water
    effective = {  0:[],
                  .5:[t.water, t.grass],
                 1.5:[t.fire, t.ground, t.rock]
                }

class Ice(Move):
    type = t.ice
    effective = {  0:[],
                  .5:[t.ice, t.water, t.steel],
                 1.5:[t.grass, t.ground, t.flying]
                }

class Fire(Move):
    type = t.fire
    effective = {  0:[],
                  .5:[t.fire, t.rock, t.water],
                 1.5:[t.grass, t.bug, t.ice, t.steel]
                }
    def __init__(self, name, power, chance):
        super().__init__(name, power)
        self.chance = chance
    def use(self, attacker, defender):
        result = super().use(attacker, defender)
        if random.randrange(100) < self.chance:
            defender.burned = 0.0625
            result += [f"-->{defender.name} is burned!"]
        return result

class Grass(Move):
    type = t.grass
    effective = {  0:[],
                  .5:[t.grass, t.fire, t.flying, t.poison, t.bug, t.steel],
                 1.5:[t.ground, t.water, t.rock]
                }

class Bug(Move):
    type = t.bug
    effective = {  0:[],
                  .5:[t.bug, t.flying, t.poison, t.fire, t.steel],
                 1.5:[t.grass]
                }

class Ground(Move):
    type = t.ground
    effective = {  0:[t.flying],
                  .5:[t.ground, t.grass, t.bug],
                 1.5:[t.rock, t.electric, t.poison, t.fire, t.steel]
                }

class Rock(Move):
    type = t.rock
    effective = {  0:[],
                  .5:[t.rock, t.ground, t.steel],
                 1.5:[t.fire, t.bug, t.flying, t.ice]
                }

class Flying(Move):
    type = t.flying
    effective = {  0:[],
                  .5:[t.flying, t.rock, t.electric],
                 1.5:[t.grass, t.bug]
                }

class Electric(Move):
    type = t.electric
    effective = {  0:[t.ground],
                  .5:[t.electric, t.grass],
                 1.5:[t.flying, t.water]
                }
    def __init__(self, name, power, chance):
        super().__init__(name, power)
        self.chance = chance
    def use(self, attacker, defender):
        result = super().use(attacker, defender)
        if random.randrange(100) < self.chance:
            defender.paralyzed = 1
            result += [f"-->{defender.name} is paralyzed!"]
        return result

class Poison(Move):
    type = t.poison
    effective = {  0:[t.steel],
                  .5:[t.poison, t.ground, t.rock],
                 1.5:[t.grass]
                }
    def __init__(self, name, power, chance, strength):
        super().__init__(name, power)
        self.chance   = chance
        self.strength = strength
    def use(self, attacker, defender):
        result = super().use(attacker, defender)
        if random.randrange(100) < self.chance:
            defender.poisoned = self.strength
            result += [f"-->{defender.name} is poisoned!"]
        return result

class Steel(Move):
    type = t.steel
    effective = {  0:[],
                  .5:[t.steel, t.fire, t.water, t.electric],
                 1.5:[t.ice, t.rock]
                }

leer          = Normal  ('leer',          1, defender=[0, 1])
tackle        = Normal  ('tackle',       40)
tail_whip     = Normal  ('tail whip',     1, defender=[0, 1])
growl         = Normal  ('growl',         1, defender=[1, 0])
scratch       = Normal  ('scratch',      40)
slash         = Normal  ('slash',        70)
bite          = Normal  ('bite',         60)
swift         = Normal  ('swift',        60)
horn_attack   = Normal  ('horn attack',  65)
harden        = Normal  ('harden',        1, attacker=1)
bubble        = Water   ('bubble',       20)
water_gun     = Water   ('water gun',    40)
ember         = Fire    ('ember',        40,  10)
flamethrower  = Fire    ('flamethrower', 95,  10)
poison_sting  = Poison  ('poison sting', 15,  20, 0.0625)
poison_powder = Poison  ('poison powder', 1, 100, 0.125)
thundershock  = Electric('thundershock', 40,  10)
thunderwave   = Electric('thundershock',  1, 100)
bug_bite      = Bug     ('bug bite',     60)
vine_whip     = Grass   ('vine whip',    35)
razor_leaf    = Grass   ('razor leaf',   55)
peck          = Flying  ('peck',         35)
