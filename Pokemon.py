import random
import Types as t
import Moves as m

class Pokemon():
    XP        = 0
    burned    = 0
    poisoned  = 0
    paralyzed = 0

    def reset(self):
        self.HP = self.base_HP
        self.defense = self.base_defense
        self.attack = self.base_attack

    def __init__(self):
        self.reset()

    def lvl(self):
        level = 0
        for i in range(0, 9):
            if self.XP >= i ** 2:
                level = i+1
        return level

    def stats(self):
        return ' '.join([ self.emoji, f'L{self.lvl()}', f"{''.join(self.type).ljust(2)}", f'{str(self.HP).rjust(2)}HP'])

    def randomXP(self, level):
        self.XP = random.randrange(level ** 2)

    def learned(self):
        learned = []
        for key in self.moves.keys():
            if self.lvl() >= key:
                learned += self.moves[key]
        return learned[-4:]

    def useMove(self, opponent, choice=-1):
        print([move.name for move in self.learned()])
        self.XP += 1
        if choice < 0:
            choice = random.randrange(len(self.learned()))
        move = self.learned()[choice]
        result = move.use(self, opponent)
        if opponent.HP <= 0:
            opponent.HP = max(0, opponent.HP)
            result += [f"-->{opponent.name} fainted!"]
        return [f"{self.name} used {move.name.upper()}!"] + result

class Bulbasaur(Pokemon):
    base_HP  = 45
    base_attack = 49
    base_defense = 49
    name    = 'Bulbasaur'
    emoji   = '🦕'
    type    = [t.grass, t.poison]
    moves   = { 1:[m.growl, m.tackle],
                3:[m.vine_whip],
                5:[m.poison_powder],
                7:[m.razor_leaf]
              }

class Squirtle(Pokemon):
    base_HP  = 44
    base_attack = 48
    base_defense = 65
    name    = 'Squirtle'
    emoji   = '🐢'
    type    = [t.water]
    moves   = { 1:[m.tackle, m.tail_whip],
                3:[m.bubble],
                5:[m.water_gun],
                7:[m.bite]
                # 9:[m.skull_bash]
              }

class Charmander(Pokemon):
    base_HP  = 39
    base_attack = 52
    base_defense = 43
    name    = 'Charmander'
    emoji   = '🦎'
    type    = [t.fire]
    moves   = { 1:[m.scratch, m.growl],
                3:[m.slash],
                5:[m.ember, m.leer],
                7:[m.flamethrower]
              }

class Pikachu(Pokemon):
    base_HP  = 35
    base_attack = 55
    base_defense = 40
    name    = 'Pikachu'
    emoji   = '🐁'
    type    = [t.electric]
    moves   = { 1:[m.growl, m.thundershock],
                3:[m.thunderwave],
                5:[m.swift]
              }

class Nidoran(Pokemon):
    base_HP  = 46
    base_attack = 47
    base_defense = 40
    name    = 'Nidoran'
    emoji   = '🐇'
    type    = [t.electric]
    moves   = { 1:[m.leer],
                3:[m.horn_attack],
                5:[m.poison_sting]
              }

class Spearow(Pokemon):
    base_HP  = 40
    base_attack = 60
    base_defense = 30
    name    = 'Spearow'
    emoji   = '🦉'
    type    = [t.normal, t.flying]
    moves   = { 1:[m.peck]
              }

class Weedle(Pokemon):
    base_HP  = 45
    base_attack = 35
    base_defense = 30
    name    = 'Weedle'
    emoji   = '🪱'
    type    = [t.bug, t.poison]
    moves   = { 1:[m.poison_sting],
                3:[m.bug_bite]
              }

class Kakuna(Pokemon):
    base_HP  = 45
    base_attack = 25
    base_defense = 50
    name    = 'Kakuna'
    emoji   = '🦪'
    type    = [t.bug, t.poison]
    moves   = { 1:[m.harden],
              }

class Caterpie(Pokemon):
    base_HP  = 45
    base_attack = 30
    base_defense = 35
    name    = 'Caterpie'
    emoji   = '🐛'
    type    = [t.bug]
    moves   = { 1:[m.tackle],
                3:[m.bug_bite]
              }

pokemon = [Bulbasaur(), Squirtle(), Charmander(), Pikachu(), Nidoran(), Spearow(), Weedle(), Caterpie()]
