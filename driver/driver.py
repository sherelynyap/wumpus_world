from map import *
from pyswip import Prolog


# There is 2 maps in this game, the Absolute map and the Relative Map
# Absolute map is the
# The Absolute map has been currently hard code in this way
# [ '!' , '!' , '!' , '!' , '!' , '!' , '!']
# [ '!' , 'P' , 'W' , '!' , 'P' , '!' , '!']
# [ '!' , '!' , '!' , '!' , 'C' , '!' , '!']
# [ '!' , '!' , '!' , '!' , '!' , '!' , '!']
# [ '!' , 'A' , '!' , '!' , '!' , 'P' , '!']
# [ '!' , '!' , '!' , '!' , '!' , '!' , '!']

# Percepts format : [ Confounded, Stench, Tingle, Glitter, Bump, Scream ]
# Actions: [ shoot, moveforward, turnleft, turnright, pickup ]


# prolog_file = 'Agent.pl'
# prolog = Prolog()
# prolog.consult(prolog_file)


def main():
    # agent_explore(prolog)
    # agent_correctness(prolog)
    agent_correctness()

def agent_explore(prolog):
    # Initialisation...
    print("Initialisation... ")
    abs_map = Abs_Map(map_x=7, map_y=6, portal=3, coin=1)
    abs_map.create_map()
    abs_map.display_abs_world('Initial Absolute Map')

    r_map = R_Map()
    r_map.display_r_world()


    # reborn = list(prolog.query("reborn."))


# Testing map update....
def agent_correctness():
    test_list = [
        # Test 01
        ['moveforward', 'moveforward', 'pickup', 'turnright', 'moveforward']
        # ['moveforward', 'moveforward', 'turnleft']
        ]
    # Reset Agent
    # reborn = list(prolog.query("reborn."))
    # Get
    # agent_action = list(prolog.query('explore(L)'))
    abs_map = Abs_Map(map_x=7, map_y=6, portal=3, coin=1)
    abs_map.create_map()
    abs_map.display_abs_world('Initial Absolute Map')
    print("Agent is starting at location: ", abs_map.agent_loc)
    agent_x = abs_map.agent_loc[0]
    agent_y = abs_map.agent_loc[1]

    # query = "reposition([" + abs_map.world_map[agent_y][agent_x].get_percepts() + "])"  # Pass percepts to agent
    # list(prolog.query(query))
    print("Initial Percepts sent to Agent: ", abs_map.world_map[agent_y][agent_x].get_percepts())
    # Send percepts to Agent!----------------------------------
    for moves in test_list:
        for move in moves:
            current_loc = abs_map.get_agentlocation()
            agent_move(move,current_loc, abs_map)
    abs_map.display_abs_world('Update Absolute Map')


def agent_move(move, current_loc, abs_map):
    agent_x = current_loc[0]
    agent_y = current_loc[1]
    agent_ori = current_loc[2]

    current_percepts = abs_map.world_map[agent_y][agent_x].get_percepts()

    if move == 'moveforward':
        new_loc = move_forward(current_loc)
        proceed = check_status(new_loc, current_loc, abs_map)
        if proceed:
            abs_map.world_map[agent_y][agent_x].set_visited()
            agent_x = new_loc[0]
            agent_y = new_loc[1]
            agent_ori = new_loc[2]
            abs_map.update_agentlocation(new_loc[0], new_loc[1], new_loc[2])
            abs_map.world_map[agent_y][agent_x].set_agent(agent_ori)
            # query = "move(moveforward,[" + abs_map.world_map[agent_y][agent_x].get_percepts() + "])"
            # list(prolog.query(query))
            print("Move Forward | Percepts sent to Agent: ", abs_map.world_map[agent_y][agent_x].get_percepts())
            print("Position updated!")
        else:
            # query = "move(moveforward,[" + abs_map.world_map[agent_y][agent_x].get_percepts() + "])"
            # list(prolog.query(query))
            print("Move Forward | Percepts sent to Agent: ", abs_map.world_map[agent_y][agent_x].get_percepts())
            print("Agent is at location: ", abs_map.agent_current_loc)

    elif move == 'pickup':
        # The percepts don't change when turning on the spot
        abs_map.world_map[agent_y][agent_x].pick_coin()
        print("Pickup | Percepts sent to Agent: ", abs_map.world_map[agent_y][agent_x].get_percepts())
        # query = "move(pickup,[" + abs_map.world_map[agent_y][agent_x].get_percepts() + "])"
        # list(prolog.query(query))


    elif move == 'turnleft':
        new_angle = (agent_ori.value - 90) % 360
        new_ori = Directions(new_angle)
        # The percepts don't change when turning on the spot
        print("Turn Left | Percepts sent to Agent: ", abs_map.world_map[agent_y][agent_x].get_percepts()  )
        # query = "move(turnleft,[" + abs_map.world_map[agent_y][agent_x].get_percepts() + "])"

        # list(prolog.query(query))

        abs_map.update_agentlocation(agent_x,agent_y,new_ori)


    elif move == 'turnright':
        new_angle = (agent_ori.value + 90) % 360
        new_ori = Directions(new_angle)
        abs_map.update_agentlocation(agent_x, agent_y, new_ori)
        print("Turn Right | Percepts sent to Agent: ", abs_map.world_map[agent_y][agent_x].get_percepts())
        # The percepts don't change when turning on the spot

        # query = "move(turnright,[" + abs_map.world_map[agent_y][agent_x].get_percepts() + "])"
        # list(prolog.query(query))


    elif move == 'shoot':
        abs_map.shoot_arrow() #Loses arrow
        print("Shoot | Percepts sent to Agent: ", abs_map.world_map[agent_y][agent_x].get_percepts())
        # The percepts don't change when turning on the spot
        # query = "move(shoot,[" + abs_map.world_map[agent_y][agent_x].get_percepts() + "])"
        # list(prolog.query(query))


def move_forward(current_loc):
    agent_x = current_loc[0]
    agent_y = current_loc[1]

    agent_orientation = current_loc[2]

    if agent_orientation == Directions.RNORTH:
        agent_y -= 1

    elif agent_orientation == Directions.REAST:
        agent_x += 1

    elif agent_orientation == Directions.RSOUTH:
        agent_y += 1

    elif agent_orientation == Directions.RWEST:
        agent_x -= 1

    return [agent_x,agent_y,agent_orientation]

def check_status(new_loc,old_loc, abs_map):
    new_x = new_loc[0]
    new_y = new_loc[1]
    x = old_loc[0]
    y = old_loc[1]

    if abs_map.world_map[new_y][new_x].wall == True:
        abs_map.world_map[y][x].set_bump()
        print("Bumped into a wall...")
        return False

    elif abs_map.world_map[new_y][new_x].portal == True:
        abs_map.reposition()
        return False
    elif abs_map.world_map[new_y][new_x].wumpus == True:
        print("You met a Wumpus, game over!")
        abs_map.reset()
        return False

    return True

main()





