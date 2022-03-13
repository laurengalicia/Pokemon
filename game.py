import random, copy
import settings as s
import unicode as u
import Pokemon, Items, Tiles

grid = Tiles.Grid(s.W, s.H)
grid = grid.tiles

def direction(key, x, y):
    coords = {
        'W': (x-1, y  ),
        'S': (x+1, y  ),
        'A': (x  , y-1),
        'D': (x  , y+1)
    }
    return coords[key]

def gridTile(key):
    X, Y = direction(key, x, y)
    return grid[X][Y]

def nav(key):
    return ' ' if gridTile(key) == Tiles.tree else '[' + key + ']'

def GridView(x, y):
    return [''.join([grid[x+h][y+w].emoji for w in range(0 - s.W, s.W + 1)]) for h in range(0 - s.H, s.H + 1)]

def Fill(caption):
    whitespace = s.height - 2 - len(caption)
    top        = int(whitespace / 2)
    bottom     = whitespace - top
    return [*[''] * (top + 1), *caption, *[''] * (bottom + 1)]

def Console(screen, caption, controls=[' ' * 9] * s.height):
    border  = '-' * ((s.W * 2 + 1) * 2)
    borders = [f' +-{border}-+ ', ' | ']
    screen  = [borders[0], *[borders[1] + s + borders[1] for s in screen], borders[0], '']
    return '\n'.join([''.join(line) for line in list(zip(*[controls, screen, Fill(caption)]))])

def Controls(controls):
    return [control.center(9) for control in controls]

def validKey(validKeys, console):
    entered = input(f'          > ').upper()
    entered = entered[0] if entered else None
    while entered not in validKeys:
        print(console)
        entered = input(f'TRY AGAIN > ').upper()
    return entered

def choiceList( category, choices, caption=''):
    header  = f"Select {category}:"
    icons   = ' '.join([f' {choice}' for choice in choices])
    indices = ' '.join([f'[{str(i+1)}]' for i in range(len(choices))])
    console = Console(GridView(*s.start), [*caption, header, icons, indices])
    print(console)
    entered = validKey([str(i+1) for i in range(len(choices))], console)
    index   = int(entered)-1
    return index, choices[index]

def index(array, value):
    for i, element in enumerate(array):
        if element == value:
            return i

class Player():
    pokemon = []
    items   = []
    def __init__(self):
        console = Console(GridView(*s.start), ['What is your name?'])
        print(console)
        entered = input(f'          > ')
        while len(entered) < 1 or len(entered) > 12:
            print(console)
            entered = input(f'TOO LONG! > ') if len(entered) > 12 else input(f'TRY AGAIN > ')
        self.name  = entered.capitalize()
        face       = choiceList('face', u.faces)
        self.skin  = u.skins[choiceList('skin', [face[1] + skin for skin in u.skins])[0]]
        self.emoji = u.standing + self.skin + u.genders[face[0]]
        self.face  = face[1] + self.skin
    def addItem(self, newItem):
        if newItem in self.items:
            for item in self.items:
                if item == newItem:
                    item.count += 1
        else:
            newItem.count = 1
            self.items += [newItem]
        return [f'{self.face} {self.name} found an item!', newItem.stats()]
    def addPokemon(self, wildPokemon):
        self.pokemon.append(copy.deepcopy(wildPokemon))
        wildPokemon.HP = wildPokemon.base_HP
        return [f'{self.face} {self.name} now has one {wildPokemon.name}']

def BattleView():
    w = s.W * 4 + 2
    enemy = f"{opponent.pokemon[0].HP}HP".rjust(w-1), f"L{opponent.pokemon[0].lvl()}".rjust(w-3)
    enemy = ['╲' + enemy[0]] + ['  ╲' + enemy[1]]
    home  = f"{player.pokemon[0].HP}HP".ljust(w-1), f"L{player.pokemon[0].lvl()}".ljust(w-3)
    home  = [home[1] + '╲  '] + [home[0] + '╲']
    return enemy + [player.pokemon[0].emoji + 'VS'.center(w-4) + opponent.pokemon[0].emoji] + home

if __name__ == "__main__":
    player = Player()
    x, y   = s.start
    X, Y   = x, y
    old_tile   = grid[x][y]
    grid[x][y] = player
    caption = [f"{player.name} is now in Viridian Forest", '']
    starter = copy.deepcopy(Pokemon.pokemon[:3][choiceList('starter type', [starter.type[0] for starter in Pokemon.pokemon[:3]], caption)[0]])
    caption = player.addPokemon(starter) + [f"{player.pokemon[0].stats()}"]
    fighting      = False
    viewPokemon   = False
    viewItems     = False
    chooseMove    = 0
    changePokemon = 0
    useItem       = 0
    actions       = []
    validKeys     = []
    while True:
        grid[X][Y] = old_tile
        old_tile   = grid[x][y]
        X, Y       = x, y
        grid[x][y] = player
        player.coords = (x, y)
        walks   = [key for key in ['W', 'A', 'S', 'D'] if nav(key) != ' ']
        navKeys = [nav('W'), nav('A') + '   ' + nav('D'), nav('S'), '']
        # for h in range(-1, 1):
        #     for w in range(-1, 1):
        #         nearby = grid[x+h][y+w]
                # if isinstance(nearby, Tiles.Trainer) and fighting == False:
                    # opponent = nearby
        if isinstance(old_tile, Tiles.Trainer):
            opponent = old_tile
            if opponent.pokemon[0].HP > 0:
                if fighting == False:
                    fighting = True
                    caption  = [f'{opponent.face} {opponent.name} wants to fight!', '', f'{opponent.name} sent out {opponent.pokemon[0].name}!']
            else:
                if len(opponent.pokemon) > 1:
                    fighting = True
                    opponent.pokemon = opponent.pokemon[1:]
                    caption = [f'{opponent.name} sent out {opponent.pokemon[0].name} {opponent.pokemon[0].emoji}!']
                else:
                    fighting = False
                    caption  = [f'{player.pokemon[0].name} gained {opponent.prize}XP!']
                    opponent = Tiles.Grass(0, 0)
        if old_tile == Tiles.hospital:
            for mon in player.pokemon:
                mon.reset()
            caption = f"All {player.name}'s Pokemon", 'restored to full HP!'
        elif old_tile == Tiles.gift:
            item = random.choice(Items.items)
            caption  = player.addItem(item)
            old_tile = Tiles.Grass(0, 0)
        elif isinstance(old_tile, Items.Ball):
            old_tile.coords = (x, y)
            caption  = player.addItem(old_tile)
            old_tile = Tiles.Grass(0, 0)
        elif isinstance(old_tile, Tiles.Grass):
            if entered in walks and fighting == False:
                if random.randrange(100) > 75 and old_tile.type != 0:
                    fighting = True
                    opponent = old_tile
                    opponent.pokemon = [random.choice(opponent.possibility[opponent.type])]
                    opponent.pokemon[0].randomXP(opponent.level)
                    opponent.pokemon[0].reset()
                    caption  = [f'Wild {opponent.pokemon[0].name.upper()} appeared!']
            if entered == 'R':
                caption = []
            if fighting and opponent == old_tile:
                actions += ['Run']
                if opponent.pokemon[0].HP <= 0:
                    fighting  = False
                    old_tile  = Tiles.Grass(old_tile.level, old_tile.type)
        views = ['Pokemon', player.pokemon, viewPokemon], ['Items', player.items, viewItems]
        for view in views:
            if view[2]:
                onScreen = view[1][n:n+min(len(view[1])-n, n+4)]
                if indexed:
                    validKeys += [str(i+1) for i in range(len(onScreen))]
                else:
                    header = [f"{player.face} {player.name}'s {view[0]}:"]
                if len(view[1]) > n + 4:
                    actions += ['More']
                if n > 0:
                    actions += ['Back']
                caption = header + [((f"[{str(i+1)}] " if indexed else (f"x{value.count} ") if view[0] == 'Items' and value.count > 1 else '') + f" {value.stats()}") for i, value in enumerate(onScreen)]
            else:
                if len(view[1]) > 0:
                    actions += [view[0]]
        if fighting:
            navKeys = []
            if chooseMove == False:
                actions += ['Fight']
        else:
            validKeys += [walk for walk in walks]
        buttons = [f'[{action[0]}]{action[1:]}' for action in actions]
        controls = []
        if player.pokemon[0].HP > 0:
            controls = navKeys + buttons
        elif len(set([mon.name for mon in player.pokemon])) > 4:
            caption += ['YOU WIN']
        else:
            caption = caption[:-1] + [caption[-1] + ' GAME OVER']
            actions = []
        validKeys += [action[0] for action in actions]
        controls = controls + [''] * (s.height - len(controls)) if navKeys else Fill(controls)
        console = Console((BattleView() if fighting else GridView(x, y)), caption, controls=Controls(controls))
        print(console)
        entered = input('          > ').upper()
        while entered not in validKeys:
            keys = ', '.join(validKeys)
            print(f'                         Choose: {keys}')
            print(console)
            entered = input('TRY AGAIN > ').upper()
        validKeys = []
        actions = []
        caption = ['']
        if entered in ['P', 'I'] and fighting == False:
            indexed = False
        if entered in ['P', 'C']:
            if len(player.pokemon) > 1:
                actions += ['Change']
        if entered in ['P', 'F', 'R']:
            useItem = 0
        if entered in [*walks, 'F']:
            n = 0
            indexed = False
            viewPokemon = False
            viewItems   = False
        i = 0
        if entered == 'M':
            n += 4
        elif entered == 'B':
            n -= 4
        elif entered in walks:
            fighting  = False
            x, y = direction(entered, x, y)
            grid[X][Y] = old_tile
            caption = ''
        elif entered == 'R':
            fighting = False
        elif entered == 'P':
            viewPokemon = True
            viewItems   = False
        elif entered == 'I':
            viewPokemon = False
            viewItems   = True
            if fighting:
                useItem = 'pre-choose'
            else:
                non_balls = 0
                for item in player.items:
                    if isinstance(item, Items.Ball) == False:
                        non_balls += 1
                if non_balls > 0:
                    actions += ['Use']
        elif entered == 'U':
            useItem = 'pre-choose'
        elif entered == 'C':
            if len(player.pokemon) == 2:
                changePokemon = 'changed'
                player.pokemon[0], player.pokemon[1] = player.pokemon[1], player.pokemon[0]
            else:
                changePokemon = 'changing'
                indexed = True
                header = [f"Move {player.pokemon[0].emoji} where?"]
        elif entered == 'F':
            fighting  = True
        else:
            i = int(entered) - 1 + n
            if changePokemon == 'changing':
                changePokemon = 'changed'
                indexed       = False
                if fighting:
                    viewPokemon = False
                    caption     = [f"{player.name} changed Pokemon"]
                else:
                    viewPokemon = True
                player.pokemon[0], player.pokemon[i] = player.pokemon[i], player.pokemon[0]
            if useItem == 'choosing item':
                useItem = 'item chosen'
                I = i
            if useItem == 'choosing pokemon':
                useItem = 'pokemon chosen'
                recipient = player.pokemon[i]
            if chooseMove == 'choosing move':
                chooseMove = 'move chosen'
                caption = player.pokemon[0].useMove(opponent.pokemon[0], choice=i)
                if opponent.pokemon[0].HP <= 0:
                    fighting = False
        if entered == 'F':
            if chooseMove != 'move chosen' or changePokemon != 'changed' or useItem != 'item used':
                chooseMove = 'choosing move'
                header = [f"Select attack for {player.pokemon[0].name} to use:"]
                moves  = [f"[{str(i+1)}] {move.name}".ljust(18) for i, move in enumerate(player.pokemon[0].learned())]
                caption = header + moves
                validKeys += [str(i+1) for i in range(len(player.pokemon[0].learned()))]
        if useItem == 'pre-choose':
            if len(player.items) == 1:
                useItem = 'item chosen'
                I = 0
            else:
                useItem = 'choosing item'
                indexed = True
                header  = ['Use which item?']
        if useItem == 'item chosen':
            item = player.items[I]
            viewItems = False
            if isinstance(item, Items.Ball):
                if fighting:
                    fighting = False
                    useItem = 'item used'
                    caption = [f"{player.name} used Poke-ball!"]
                    if random.randrange(opponent.pokemon[0].base_HP) > opponent.pokemon[0].HP:
                        caption += [f"--> {opponent.pokemon[0].name} was caught!", '']
                        caption += player.addPokemon(opponent.pokemon[0])
                        opponent = Tiles.Grass(0, 0)
                    else:
                        caption += ['--> missed!']
                        grid[item.coords[0]][item.coords[1]] = Items.pokeball
                else:
                    useItem = 'pre-choose'
                    caption = [f"{item.name} can't be", 'used right now']
            else:
                if len(player.pokemon) == 1:
                    useItem   = 'pokemon chosen'
                    recipient = player.pokemon[0]
                else:
                    useItem     = 'choosing pokemon'
                    viewPokemon = True
                    indexed = True
                    header  = [f"Select Pokemon to use {item.name} on:"]
        if useItem == 'pokemon chosen':
            useItem = 'item used'
            caption = [f"{player.name} used {item.name}!"] + item.use(recipient)
        if useItem == 'item used':
            indexed = False
            item.count -= 1
            if item.count == 0:
                player.items = player.items[:I] + player.items[I+1:]
        if chooseMove == 'move chosen' or changePokemon == 'changed' or useItem == 'item used':
            if fighting:
                move = opponent.pokemon[0].useMove(player.pokemon[0])
                caption += ['', 'Enemy ' + move[0]] + move[1:]
            chooseMove    = 0
            changePokemon = 0
            useItem       = 0
