from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

def room_starting_value(visited, room):
    num_possible_exits = room.get_exits()

    visited[room.id] = {}

    for possible in num_possible_exits:
        visited[room.id][possible] = "?"

def num_remaining_paths(room):
    num_unexplored_exits = 0

    for direction in room:
        if room[direction] == "?":
            num_unexplored_exits += 1

    return num_unexplored_exits

inverse_directions = {
    "e": "w",
    "w": "e",
    "s": "n",
    "n": "s"
}



def do_traversal(maze, player):
    rooms_visited = {}
    directions_reversed = []
    directions_result = []
    room_starting_value(rooms_visited, player.current_room)

    while len(rooms_visited) < len(room_graph):
        if num_remaining_paths(rooms_visited[player.current_room.id]) > 0:
            for move in player.current_room.get_exits():
                if rooms_visited[player.current_room.id][move] == "?":
                    prev_room_id = player.current_room.id
                    backtrack_move = inverse_directions[move]
                    player.travel(move)
                    directions_result.append(move)
                    directions_reversed.append(backtrack_move)
                    rooms_visited[prev_room_id][move] = player.current_room.id

                    if player.current_room.id not in rooms_visited:
                        room_starting_value(
                            rooms_visited, player.current_room)
                    rooms_visited[player.current_room.id][backtrack_move] = prev_room_id
                    break

        else:
            backtrack_move = directions_reversed.pop()
            player.travel(backtrack_move)
            directions_result.append(backtrack_move)

    return directions_result

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = do_traversal(world, player)



# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
