class Item():
    def __init__(self, emoji, name):
        self.name = name
        self.emoji = emoji
    def stats(self):
        return ' '.join([self.emoji, self.name.ljust(9)])

class Ball(Item):
    pass

class Heal(Item):
    def __init__(self, emoji, name, status):
        super().__init__(emoji, name)
        self.status = status
    def use(self, pokemon):
        statuses = [pokemon.burned, pokemon.poisoned, pokemon.paralyzed]
        for i, status in ['burned', 'poisoned', 'paralyzed']:
            if self.status == status:
                statuses[i] = 0
                return [f"{pokemon.name} is no longer {status}!"]

class Restore(Item):
    def __init__(self, emoji, name, HP):
        super().__init__(emoji, name)
        self.HP = HP
    def stats(self):
        return super().stats() + f" +{self.HP}HP"
    def use(self, pokemon):
        pokemon.HP += self.HP
        pokemon.HP = min(100, pokemon.HP)
        return [f"{pokemon.name} now has {self.HP}HP!"]

pokeball     = Ball('๐ด', 'Poke-ball')
burn_heal    = Heal('๐ฉน', 'Burn Heal', 'burned')
antidote     = Heal('๐', 'Antidote', 'poisoned')
paralyz_heal = Heal('๐', 'Parlyz Heal', 'paralyzed')
potion       = Restore('๐งช', 'Potion', 20)
revive       = Restore('๐', 'Revive', 50)

items = [antidote, burn_heal, paralyz_heal, potion, revive]
