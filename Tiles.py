import random, copy
import unicode as u
import Pokemon as p
from Items import pokeball

class Tile():
    def __init__(self, emoji):
        self.emoji = emoji

class Grass(Tile):
    emoji = '🌱'
    possibility = {
        1: [p.Weedle() ]*5 + [p.Caterpie()]*5,
        2: [p.Weedle() ]*3 + [p.Caterpie()]*3 + [p.Nidoran()]*4,
        3: [p.Nidoran()]*8 + [p.Pikachu() ]*2
    }
    def __init__(self, level, type):
        self.level = level
        self.type  = type

class Trainer():
    def __init__(self, level):
        _skins = [skin for skin in u.skins]
        names = ['Youngster', 'Bug Catcher', 'Red', 'Leaf', 'Avery']
        random.shuffle(copy.deepcopy(u.skins))
        random.shuffle(names)
        gender = random.randrange(3)
        self.gender = u.genders[gender]
        self.skin = _skins[level-1]
        self.emoji = u'\U0001f64b' + self.skin + self.gender
        self.face = u.faces[gender] + self.skin
        self.name = names[level-1]
        self.prize = level * 10
        self.pokemon = random.sample((copy.deepcopy(p.pokemon)), level + 1)
        for mon in self.pokemon:
            mon.randomXP(level)

tree     = Tile('🌳')
path     = Tile('⬜️')
gift     = Tile('🎁')
hospital = Tile('🏥')

class Grid():
    def __init__(self, W, H):
        tiles = [
            [ path,       Grass(3,3), tree,       path,       path,       path,       tree,       path,       path,       path,       path,       path,       path       ],
            [ path,       Grass(3,3), tree,       path,       tree,       path,       tree,       Grass(3,2), tree,       tree,       tree,       tree,       path       ],
            [ Grass(3,3), Grass(3,3), tree,       Grass(3,2), tree,       Grass(3,2), tree,       Grass(3,2), Grass(4,3), Grass(4,3), path,       path,       path       ],
            [ Grass(3,3), Grass(4,3), tree,       Grass(3,2), tree,       Grass(3,2), tree,       Grass(3,2), tree,       tree,       gift,       tree,       Grass(4,2) ],
            [ Grass(5,3), Grass(5,3), tree,       Grass(3,2), tree,       Grass(3,2), Trainer(4), Grass(3,2), tree,       tree,       path,       tree,       pokeball   ],
            [ Grass(5,3), Trainer(5), tree,       Grass(3,2), tree,       path,       path,       path,       tree,       tree,       path,       path,       Trainer(3) ],
            [ Grass(4,3), Grass(5,3), path,       Grass(3,2), tree,       tree,       tree,       tree,       tree,       Grass(3,1), Grass(3,2), tree,       path       ],
            [ path,       path,       path,       path,       path,       tree,       tree,       tree,       tree,       Grass(3,1), Grass(3,2), tree,       path       ],
            [ tree,       tree,       tree,       tree,       gift,       tree,       tree,       tree,       tree,       Grass(3,1), Grass(3,2), tree,       path       ],
            [ pokeball,   Grass(3,1), Grass(2,2), Grass(2,2), tree,       tree,       tree,       tree,       tree,       Grass(3,1), Grass(3,2), tree,       path       ],
            [ tree,       tree,       path,       Grass(2,1), Grass(2,1), Grass(2,1), path,       Grass(3,1), tree,       Grass(2,1), path,       path,       Trainer(2) ],
            [ tree,       tree,       path,       Grass(2,1), tree,       Grass(2,1), path,       Grass(3,1), tree,       Grass(2,1), path,       tree,       tree       ],
            [ Trainer(1), Grass(2,1), path,       Grass(2,1), Grass(2,1), Grass(2,1), path,       Grass(2,1), Grass(2,1), Grass(2,1), path,       Grass(4,1), Grass(4,1) ],
            [ Grass(2,1), Grass(2,1), path,       path,       path,       path,       path,       path,       path,       path,       path,       Grass(4,1), pokeball   ],
            [ tree,       tree,       tree,       tree,       tree,       gift,       path,       pokeball,   tree,       tree,       tree,       tree,       tree       ],
            [ tree,       tree,       tree,       tree,       tree,       tree,       hospital,   tree,       tree,       tree,       tree,       tree,       tree       ],
        ]
        tiles = [[tree] * W + row + [tree] * W for row in tiles]
        tiles = [[tree] * len(tiles[0])] * H + tiles + [[tree] * len(tiles[0])] * H
        self.tiles = tiles
    def view(self):
        print('\n'.join([''.join([tile.emoji for tile in self.tiles[i]]) for i in range(len(self.tiles))]))
