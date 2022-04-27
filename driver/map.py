#Driver for Project (Size of 7 X 6)
# Map --> One Coin, One Agent, One Wumpus, Tree Portals

# Importing necessary libraries
import random
import math
from enum import Enum

class Directions(Enum):
        RNORTH= 0
        REAST= 90
        RSOUTH =  180
        RWEST = 270

class Abs_Map:


    def __init__(self, map_x, map_y, portal, coin, wumpus = 1, agent = 1):
        # Creation of array of world of mapsize_x and mapsize_y
        # What we know in map ----------------------------------------------
        self.map_x = map_x
        self.map_y = map_y

        # Elements
        self.portal = portal
        self.portal_loc = []

        self.coin = coin
        self.coin_loc = []

        self.wumpus = wumpus
        self.wumpus_killed = False
        self.wumpus_loc = []

        self.agent = agent
        self.agent_loc = []
        self.agent_current_loc = []
        self.agent_current_orientation = Directions.RNORTH
        self.agent_arrow = 1

        self.world_map = []


    def get_agentlocation(self):
        return self.agent_current_loc

    def update_agentlocation(self, x, y, orientation):
        self.agent_current_loc = [x, y, orientation]
        self.world_map[y][x].set_agent(orientation)

    def generate_elements_fixed(self):
        # Fixed
        self.portal_loc = [[1, 1], [4, 1], [5, 4]]
        self.coin_loc = [4, 2]
        self.wumpus_loc = [2, 1]
        self.agent_loc = [1, 4, self.agent_current_orientation]
        self.agent_current_loc = self.agent_loc

    def create_map(self):
            self.generate_elements_fixed()
            for y in range(self.map_y):
                x_list = []
                for x in range(self.map_x):
                    if y == 0 or x == 0 or y == self.map_y-1 or x == self.map_x-1:
                        x_list.append(MapCell(wall=True))
                    else:
                        x_list.append(MapCell(wall=False))
                self.world_map.append(x_list)


            pos = self.wumpus_loc
            self.world_map[pos[1]][pos[0]].wumpus_located()
            self.setAdjacentCells(pos[0], pos[1], 'stench')

            pos = self.coin_loc
            self.world_map[pos[1]][pos[0]].set_glitter()

            pos = self.portal_loc
            for loc in pos:
                self.world_map[loc[1]][loc[0]].portal_located()
                self.setAdjacentCells(loc[0],loc[1],'tingle')

            pos = self.agent_loc
            self.world_map[pos[1]][pos[0]].set_agent(pos[2])
            self.world_map[pos[1]][pos[0]].set_confounded()

            print("Map is initialised!")
            print("The location of agent is: ", self.agent_loc, " with orientation: ", self.agent_current_orientation)
            print("The location of portal is: ", self.portal_loc)
            print("The location of the coin is: ", self.coin_loc)
            print("The location of the wumpus is: ", self.wumpus_loc)




    def setAdjacentCells(self, pos_x,pos_y,type):
        if type == 'stench':
            # print('Setting Adjacent cells for stench...')
            self.world_map[pos_y-1][pos_x].set_stench()
            self.world_map[pos_y +1][pos_x].set_stench()
            self.world_map[pos_y][pos_x+1].set_stench()
            self.world_map[pos_y][pos_x-1].set_stench()

        elif type == 'tingle':
            # print('Setting Adjacent cells for tingle...')
            self.world_map[pos_y - 1][pos_x].set_tingle()
            self.world_map[pos_y + 1][pos_x].set_tingle()
            self.world_map[pos_y][pos_x + 1].set_tingle()
            self.world_map[pos_y][pos_x - 1].set_tingle()

    def removeAdjacentCells(self, pos_x,pos_y,type):
        if type == 'stench':
            # print('Setting Adjacent cells for stench...')
            self.world_map[pos_y-1][pos_x].remove_stench()
            self.world_map[pos_y +1][pos_x].remove_stench()
            self.world_map[pos_y][pos_x+1].move_stench()
            self.world_map[pos_y][pos_x-1].remove_stench()

    def reset(self):
        self.create_map()

    # Stepped onto the portal...
    def reposition(self):
        # Respawn to new place
        x = random.randint(1, self.map_x - 2)
        y = random.randint(1, self.map_y - 2)

        while self.get_safe(self.world_map[y][x]):
            x = random.randint(1, self.map_x - 2)
            y = random.randint(1, self.map_y - 2)

        self.update_agentlocation(x,y,Directions.RNORTH)


    def get_safe(self, map):
        if map.wumpus == False and map.confounded == False:
            return True
        else:
            return False




    def reset_values(self, map_x,map_y, portal, coin=1, agent=1, wumpus=1):
        # What we know in map ----------------------------------------------
        self.map_x = map_x
        self.map_y = map_y


        # Elements
        self.portal = portal
        self.portal_loc = []

        self.coin = coin
        self.coin_loc = []

        self.wumpus = wumpus
        self.wumpus_loc = []

        self.agent = agent
        self.agent_loc = []
        self.agent_current_orientation = Directions.RNORTH

        self.world_map = []
        self.reset()

    def print_world(self):
        print("===== << ABSOLUTE MAP >> ======")
        for y in range(self.map_y):
            print('ROW', y)
            for x in range(self.map_x):
                self.world_map[y][x].print_cell_grid()
                print('')
            print('---------------------')

    def print_world(self):
        print("===== << ABSOLUTE MAP >> ======")
        for y in range(self.map_y):
            print('ROW', y)
            for x in range(self.map_x):
                self.world_map[y][x].print_cell_grid()
                print('')
            print('---------------------')

    def display_abs_world(self, header):
        print('===== <<', header ,'>> ======',)
        count = 0

        for y in range(self.map_y): # 6 0,1,2,3,4,5,6
            while count < 3:
                for x in range(self.map_x): # 7 0,1,2,3,4,5,6,7
                    print(self.world_map[y][x].cell_grid[count], '      ', end=' ')
                print('----')
                count += 1
            print()
            count = 0





class MapCell:

    def __init__(self,wall):
        # Sensory Input
        self.confounded = False
        self.stench = False
        self.tingle = False
        self.glitter = False
        self.bump = False
        self.scream = False
        self.portal = False

        # Locations Predictions
        self.wumpus = False
        self.portal = False
        self.wall = False
        self.visited = False


        self.facing = { Directions.RNORTH: '^',
                   Directions.RSOUTH : 'V',
                   Directions.REAST : '>',
                   Directions.RWEST: '<'
                   }
        self.symbol1 = [0,0]
        self.symbol2 = [0, 1]
        self.symbol3 = [0,2]
        self.symbol4 = [1,0]
        self.symbol5 = [1,1]
        self.symbol6 = [1,2]
        self.symbol7 = [2,0]
        self.symbol8 = [2,1]
        self.symbol9 = [2,2]

        # Initialise 3 X 3 Symbols
        if wall == False:
            self.cell_grid = [['.', '.', '.'],
                              ['.', '?', '.'],
                              ['.', '.', '.']]
            self.wall = False
        else:
            self.wall = True
            self.cell_grid = [['#','#','#'],
                              ['#','#','#'],
                              ['#','#','#']]


    def wumpus_located(self):
        self.wumpus = True
        self.cell_grid[self.symbol5[0]][self.symbol5[1]] = 'W'
        self.cell_grid[self.symbol4[0]][self.symbol4[1]] = '-'
        self.cell_grid[self.symbol6[0]][self.symbol6[1]] = '-'

    def set_glitter(self):
        self.glitter = True
        self.cell_grid[self.symbol7[0]][self.symbol7[1]] = '*'
        self.cell_grid[self.symbol4[0]][self.symbol4[1]] = '-'
        self.cell_grid[self.symbol6[0]][self.symbol6[1]] = '-'

    def portal_located(self):
        self.confounded = True
        self.portal = True
        self.cell_grid[self.symbol5[0]][self.symbol5[1]] = 'O'
        self.cell_grid[self.symbol4[0]][self.symbol4[1]] = '-'
        self.cell_grid[self.symbol6[0]][self.symbol6[1]] = '-'
    def set_tingle(self):
        self.tingle = True
        self.cell_grid[self.symbol3[0]][self.symbol3[1]] = 'T'


    def set_stench(self):
        self.stench = True
        self.cell_grid[self.symbol2[0]][self.symbol2[1]]= '='

    def set_scream(self):
        self.scream = True
        self.cell_grid[self.symbol9[0]][self.symbol9[1]] = '@'

    def set_bump(self):
        self.bump = True
        self.cell_grid[self.symbol8[0]][self.symbol8[1]] = 'B'

    def remove_bump(self):
        self.bump = False
        self.cell_grid[self.symbol8[0]][self.symbol8[1]] = '.'

    def place_agent(self,orientation):
        self.cell_grid[self.symbol4[0]][self.symbol4[1]] = '-'
        self.cell_grid[self.symbol5[0]][self.symbol5[1]] = self.facing[orientation]
        self.cell_grid[self.symbol6[0]][self.symbol6[1]] = '-'
        self.set_confounded()

    def set_agent(self,orientation):
        self.cell_grid[self.symbol5[0]][self.symbol5[1]] = self.facing[orientation]


    def set_confounded(self):
        self.confounded = True
        self.cell_grid[self.symbol1[0]][self.symbol1[1]] = '%'

    def set_safe(self):
        self.cell_grid[self.symbol5[0]][self.symbol5[1]] = 's'

    def set_visited(self):
        self.cell_grid[self.symbol5[0]][self.symbol5[1]] = 'S'

    def pick_coin(self):
        if self.glitter == True:
            self.remove_glitter()
        else:
            print("There is no coin in this cell...")

    def remove_glitter(self):
        self.glitter = False
        self.cell_grid[self.symbol7[0]][self.symbol7[1]] = '-'
        self.cell_grid[self.symbol4[0]][self.symbol4[1]] = 'S'
        self.cell_grid[self.symbol6[0]][self.symbol6[1]] = '-'


    def wumpus_killed(self):
        self.wumpus = False
        self.cell_grid[self.symbol4[0]][self.symbol4[1]] = '.'
        self.cell_grid[self.symbol5[0]][self.symbol5[1]] = 's'
        self.cell_grid[self.symbol6[0]][self.symbol6[1]] = '.'

    # In the case, wumpus has died
    def remove_stench(self):
        self.stench = False
        self.cell_grid[self.symbol2[0]][self.symbol2[1]] = '.'

    def print_cell_grid(self):
        for x in range(len(self.cell_grid)):
            print(self.cell_grid[x])
        print(',', end=' ')

    def display_cell_grid(self,col,row):
        print(self.cell_grid[col][row])

    def get_percepts(self):
        percept_list = self.convert_list([self.confounded, self.stench, self.tingle, self.glitter, self.bump, self.scream])
        return percept_list

    def convert_list(self,percept):
        percept_list = []
        for x in range(len(percept)):
            if percept[x] == True:
                percept_list.append('on')
            else:
                percept_list.append('off')
        return percept_list




class R_Map:

    def __init__(self):
        # Creation of array of world of mapsize_x and mapsize_y
        # What we know in map ----------------------------------------------

        #Initialise...
        self.map_xsize = 3
        self.map_ysize = 3

        self.center_x = math.floor(self.map_xsize // 2)
        self.center_y = math.floor(self.map_xsize // 2)

        self.relative_map = []

        for y in range(self.map_ysize):
            x_list = []
            for x in range(self.map_xsize):
                    x_list.append(MapCell(wall=False))
            self.relative_map.append(x_list)
        self.relative_map[self.center_y][self.center_x].set_agent('rnorth')

    def print_rworld(self):
        print("===== << RELATIVE MAP >> ======")
        for y in range(self.map_ysize):
            print('ROW', y)
            for x in range(self.map_xsize):
                self.relative_map[y][x].print_cell_grid()
                print('')
            print('---------------------')

    def display_r_world(self):
        print("===== << RELATIVE MAP >> ======")
        count = 0

        for y in range(self.map_ysize):  # 6 0,1,2,3,4,5,6
            while count < 3:
                for x in range(self.map_xsize):  # 7 0,1,2,3,4,5,6,7
                    print(self.relative_map[y][x].cell_grid[count], '      ', end=' ')
                print('----')
                count += 1
            print()
            count = 0
















