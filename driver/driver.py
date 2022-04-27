from map import *
import sys
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


prolog_file = '../Agent.pl'
prolog = Prolog()
prolog.consult(prolog_file)


def main():
    agent_explore(prolog)
    agent_correctness(prolog)
    filename = "TeamKJS-testPrintout-Self-Self.txt"
    sys.stdout = open(file=filename, mode="w+", encoding="utf8")


def agent_explore(prolog):
    # Initialisation...
    print("Initialisation | Explore(L)... ")
    reborn = list(prolog.query("reborn."))

    abs_map = Abs_Map(map_x=7, map_y=6, portal=3, coin=1)
    abs_map.create_map()
    abs_map.display_abs_world('Initial Absolute Map')
    agent_x = abs_map.agent_loc[0]
    agent_y = abs_map.agent_loc[1]
    query = "reposition(" + str(abs_map.world_map[agent_y][agent_x].get_percepts()) + ")"
    list(prolog.query(query))

    agent_actions = list(prolog.query('explore(L)'))
    print("Action received:", agent_actions)

    generate_rmap()


    for moves in agent_actions:
        for move in moves:
            current_loc = abs_map.get_agentlocation()
            agent_move(move, current_loc, abs_map)
        abs_map.display_abs_world('Updated Absolute Map')


# Testing map update....
def agent_correctness(prolog):
    test_list = [
        ['moveforward', 'moveforward', 'pickup', 'turnright', 'moveforward', 'turnleft', 'shoot'], # This action will kill the wumpus
        ['moveforward', 'moveforward', 'turnleft', 'moveforward', 'turnright', 'turnright', 'moveforward',
         'moveforward', 'moveforward', 'pickup']  # Action will pick up the coin
    ]
    # Reset Agent
    abs_map = Abs_Map(map_x=7, map_y=6, portal=3, coin=1)
    abs_map.create_map()
    abs_map.display_abs_world('Initial Absolute Map')
    print("Agent is starting at location: ", abs_map.agent_loc)
    agent_x = abs_map.agent_loc[0]
    agent_y = abs_map.agent_loc[1]

    query = "reposition(" + str(abs_map.world_map[agent_y][agent_x].get_percepts()) + ")"
    list(prolog.query(query))
    # print("Start Game | Initial Percepts sent to Agent: ", abs_map.world_map[agent_y][agent_x].get_percepts())
    print("Start Game | Percepts summary: ", convert_perceptlist(abs_map.world_map[agent_y][agent_x].get_percepts()))
    # Send percepts to Agent!----------------------------------
    for moves in test_list:
        print("The series of actions taken is: ", moves)
        for move in moves:
            current_loc = abs_map.get_agentlocation()
            agent_move(move, current_loc, abs_map)
            abs_map.display_abs_world('Update Absolute Map')

        print("<< --------- NEW SET OF ACTIONS ------------ >>")
        abs_map.reset()
        abs_map.display_abs_world('Initial Absolute Map')

        reborn = list(prolog.query("reborn."))

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
            query = "move(moveforward," + str(abs_map.world_map[agent_y][agent_x].get_percepts()) + ")"
            list(prolog.query(query))

            # print("Move Forward | Percepts sent to Agent: ", abs_map.world_map[agent_y][agent_x].get_percepts())
            print("Move Forward | Percepts summary: ",
                  convert_perceptlist(abs_map.world_map[agent_y][agent_x].get_percepts()))
            print("Position updated!")
        else:
            query = "move(moveforward," + str(abs_map.world_map[agent_y][agent_x].get_percepts()) + ")"
            list(prolog.query(query))
            # print("Move Forward (Bump/Portal/Wumpus) | Percepts sent to Agent: ", abs_map.world_map[agent_y][agent_x].get_percepts())
            print("Move Forward (Bump/Portal/Wumpus) | Percepts summary: ",
                  convert_perceptlist(abs_map.world_map[agent_y][agent_x].get_percepts()))
            print("Agent is at location: ", abs_map.agent_current_loc)

    elif move == 'pickup':
        # The percepts don't change when turning on the spot
        coin = abs_map.world_map[agent_y][agent_x].pick_coin()
        if (coin):
            abs_map.coin -= 1
        # print("Pickup | Percepts sent to Agent: ", abs_map.world_map[agent_y][agent_x].get_percepts())
        print("Pickup | Percepts summary: ", convert_perceptlist(abs_map.world_map[agent_y][agent_x].get_percepts()))
        query = "move(pickup," + str(abs_map.world_map[agent_y][agent_x].get_percepts()) + ")"
        list(prolog.query(query))


    elif move == 'turnleft':
        new_angle = (agent_ori.value - 90) % 360
        new_ori = Directions(new_angle)
        # The percepts don't change when turning on the spot
        # print("Turn Left | Percepts sent to Agent: ", abs_map.world_map[agent_y][agent_x].get_percepts())
        print("Turn Left | Percepts summary: ", convert_perceptlist(abs_map.world_map[agent_y][agent_x].get_percepts()))
        query = "move(turnleft," + str(abs_map.world_map[agent_y][agent_x].get_percepts()) + ")"
        list(prolog.query(query))

        abs_map.update_agentlocation(agent_x, agent_y, new_ori)


    elif move == 'turnright':
        new_angle = (agent_ori.value + 90) % 360
        new_ori = Directions(new_angle)
        abs_map.update_agentlocation(agent_x, agent_y, new_ori)
        # print("Turn Right | Percepts sent to Agent: ", abs_map.world_map[agent_y][agent_x].get_percepts())
        print(
            "Turn Right | Percepts summary: ", convert_perceptlist(abs_map.world_map[agent_y][agent_x].get_percepts()))
        # The percepts don't change when turning on the spot

        query = "move(turnright," + str(abs_map.world_map[agent_y][agent_x].get_percepts()) + ")"
        list(prolog.query(query))



    elif move == 'shoot':
        abs_map.shoot_arrow()  # Loses arrow
        agent_current = abs_map.get_agentlocation()
        current_x = agent_current[0]
        current_y = agent_current[1]
        current_ori = agent_current[2]
        wumpus_loc = abs_map.wumpus_loc
        print("Shoot | Agent is currently at : ", agent_current)
        if agent_current[2] == Directions.RNORTH:
            # If agent is facing north...
            if abs_map.wumpus_loc[0] == current_x:
                if current_y > abs_map.wumpus_loc[1]:
                    abs_map.world_map[current_y][current_x].set_scream()
                    abs_map.world_map[wumpus_loc[1]][wumpus_loc[0]].wumpus_killed()
                    abs_map.removeAdjacentCells(wumpus_loc[0], wumpus_loc[1], 'stench')
                else:
                    print("Shoot | No scream heard...")
            else:
                print("Shoot | No scream heard...")

        elif agent_current[2] == Directions.REAST:
            # If agent is facing north...
            if abs_map.wumpus_loc[1] == current_y:
                if current_x < abs_map.wumpus_loc[0]:
                    abs_map.world_map[current_y][current_x].set_scream()
                    abs_map.world_map[wumpus_loc[1]][wumpus_loc[0]].wumpus_killed()
                    abs_map.removeAdjacentCells(wumpus_loc[0], wumpus_loc[1], 'stench')
                else:
                    print("Shoot | No scream heard...")

            else:
                print("Shoot | No scream heard...")


        elif agent_current[2] == Directions.RSOUTH:
            # If agent is facing north...
            if abs_map.wumpus_loc[0] == current_x:
                if current_y < abs_map.wumpus_loc[1]:
                    abs_map.world_map[current_y][current_x].set_scream()
                    abs_map.world_map[wumpus_loc[1]][wumpus_loc[0]].wumpus_killed()
                    abs_map.removeAdjacentCells(wumpus_loc[0], wumpus_loc[1], 'stench')
                else:
                    print("Shoot | No scream heard...")

            else:
                print("Shoot | No scream heard...")

        elif agent_current[2] == Directions.RWEST:
            if abs_map.wumpus_loc[1] == current_y:
                if current_x > abs_map.wumpus_loc[0]:
                    abs_map.world_map[current_y][current_x].set_scream()
                    abs_map.world_map[wumpus_loc[1]][wumpus_loc[0]].wumpus_killed()
                    abs_map.removeAdjacentCells(wumpus_loc[0], wumpus_loc[1], 'stench')
                else:
                    print("Shoot | No scream heard...")
            else:
                print("Shoot | No scream heard...")

        # print("Shoot | Percepts sent to Agent: ", abs_map.world_map[agent_y][agent_x].get_percepts())
        print("Shoot | Percepts summary: ", convert_perceptlist(abs_map.world_map[agent_y][agent_x].get_percepts()))
        # The x, y percepts don't change when shooting

        query = "move(shoot," + str(abs_map.world_map[agent_y][agent_x].get_percepts()) + ")"
        list(prolog.query(query))


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

    return [agent_x, agent_y, agent_orientation]


def check_status(new_loc, old_loc, abs_map):
    new_x = new_loc[0]
    new_y = new_loc[1]
    x = old_loc[0]
    y = old_loc[1]

    if abs_map.world_map[new_y][new_x].wall == True:
        abs_map.world_map[y][x].set_bump()
        print("Bumped into a wall...")
        return False

    elif abs_map.world_map[new_y][new_x].portal == True:
        abs_map.world_map[y][x].remove_agent()
        abs_map.reposition()
        print("Stepped into the portal...")
        agent_x = abs_map.agent_current_loc[0]
        agent_y = abs_map.agent_current_loc[1]

        query = "reposition(" + str(abs_map.world_map[_y][agent_x].get_percepts()) + ")"
        list(prolog.query(query))
        return False

    elif abs_map.world_map[new_y][new_x].wumpus == True:
        print("You met a Wumpus, game over!")
        abs_map.reset()
        reborn = list(prolog.query("reborn."))
        return False

    return True


def convert_perceptlist(p):
    percepts = p
    if percepts[0] == 'on':
        percepts[0] = 'Confounded'
    else:
        percepts[0] = 'C'

    if percepts[1] == 'on':
        percepts[1] = 'Stench'
    else:
        percepts[1] = 'S'

    if percepts[2] == 'on':
        percepts[2] = 'Tingle'
    else:
        percepts[2] = 'T'

    if percepts[3] == 'on':
        percepts[3] = 'Glitter'
    else:
        percepts[3] = 'G'

    if percepts[4] == 'on':
        percepts[4] = 'Bump'
    else:
        percepts[4] = 'B'

    if percepts[5] == 'on':
        percepts[5] = 'Scream'
    else:
        percepts[5] = 'S'

    return '-'.join(percepts)


def generate_rmap():  # Printing Agent Knowledge map...
    query_visited = list(prolog.query("visited(X,Y)"))
    query_wumpus = list(prolog.query("wumpus(X,Y)"))
    query_portal = list(prolog.query("confundus(X,Y)"))
    query_tingle = list(prolog.query("tingle(X,Y)"))
    query_glitter = list(prolog.query("glitter(X,Y)"))
    query_stench = list(prolog.query("stench(X,Y)"))
    query_safe = list(prolog.query("safe(X,Y)"))
    query_wall = list(prolog.query("wall(X,Y)"))

    visited_x = [abs(x["X"]) for x in query_visited]
    visited_y = [abs(y["Y"]) for y in query_visited]
    max_x = max(visited_x)
    max_y = max(visited_y)

    r = R_Map(2 * (max_y + 1) + 1, 2 * (max_x + 1) + 1)
    center_x = r.relative_map.center_x
    center_y = r.relative_map.center_y
    for predict in query_wumpus:
         x = predict['X']
         y = predict['Y']
         r.relative_map[center_y + y][center_x + x].set_wumpus()

    for predict in query_tingle:
         x = predict['X']
         y = predict['Y']
         r.relative_map[center_y + y][center_x + x].set_tingle()

    for predict in query_portal:
        x = predict['X']
        y = predict['Y']
        r.relative_map[center_y + y][center_x + x].set_portal()

    for predict in query_glitter:
        x = predict['X']
        y = predict['Y']
        r.relative_map[center_y + y][center_x + x].set_glitter()

    for predict in query_stench:
        x = predict['X']
        y = predict['Y']
        r.relative_map[center_y + y][center_x + x].set_stench()

    for predict in query_safe:
        x = predict['X']
        y = predict['Y']
        r.relative_map[center_y + y][center_x + x].set_safe()

    for predict in query_wall:
        x = predict['X']
        y = predict['Y']
        r.relative_map[center_y + y][center_x + x].set_wall()





    # N x M where both numbers are always ODD


    pass


main()
