import argparse
import logging
import os
import sys
import time

import numpy as np
import pandas

from BTinterface import BTInterface
from maze import Action, Maze
from score import Scoreboard, ScoreboardFake

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

log = logging.getLogger(__name__)

# TODO : Fill in the following information
TEAM_NAME = "Hello"
SERVER_URL = "http://140.112.175.18:5000/"
MAZE_FILE = "data/small_maze3.csv"
BT_PORT = "COM5"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="0: treasure-hunting, 1: self-testing", type=str)
    parser.add_argument("--maze-file", default=MAZE_FILE, help="Maze file", type=str)
    parser.add_argument("--bt-port", default=BT_PORT, help="Bluetooth port", type=str)
    parser.add_argument(
        "--team-name", default=TEAM_NAME, help="Your team name", type=str
    )
    parser.add_argument("--server-url", default=SERVER_URL, help="Server URL", type=str)
    return parser.parse_args()


def main(mode: int, bt_port: str, team_name: str, server_url: str, maze_file: str):
    maze = Maze(maze_file)
    #point = Scoreboard(team_name, server_url)
    point = ScoreboardFake("your team name", "data/fakeUID.csv") # for local testing
    #interface = BTInterface(port=bt_port)
    # TODO : Initialize necessary variables

    if mode == "0":
        log.info("Mode 0: For treasure-hunting")
        # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible
        bluetooth = BTInterface(port=bt_port)
        bluetooth.start()
        print("bt Start")
        #moving_list = [Action.START,Action.ADVANCE,Action.U_TURN,Action.TURN_LEFT,Action.U_TURN,Action.ADVANCE,Action.U_TURN,Action.TURN_RIGHT,Action.HALT]
        #moving_list = [Action.START,Action.U_TURN,Action.HALT]
        # moving_list = [Action.START,Action.TURN_RIGHT,Action.ADVANCE,Action.U_TURN,Action.TURN_RIGHT,Action.ADVANCE,Action.U_TURN,Action.TURN_RIGHT,Action.TURN_LEFT,Action.TURN_RIGHT,Action.U_TURN,Action.TURN_RIGHT,Action.HALT]
        moving_list = maze.solveMaze()
        print(moving_list)
        bluetooth.send_action(moving_list[0])
        time.sleep(0.3)
        bluetooth.send_action(moving_list[1])
        step = 2
        while(step<len(moving_list)):
            data = bluetooth.get_data()
            if(len(data) == 2):
                bluetooth.send_action(moving_list[step])
                print("Step sent : ",moving_list[step])
                step+=1
            elif(len(data)>2 and len(data) <= 8): 
                print(data)
                point.add_UID(data)
            elif(len(data)>8):
                bluetooth.send_action(moving_list[step])
                step+=1
                data = data[0:-4]
                print(data)
                point.add_UID(data)
        time.sleep(3)
        data = bluetooth.get_data()
        if(len(data)>2 and len(data) <= 8):
            print(data)
            point.add_UID(data)
        bluetooth.end_process()
        print("Score:",point.get_current_score())
        

    elif mode == "1":
        log.info("Mode 1: Self-testing mode.")
        # TODO: You can write your code to test specific function.
        # for i in range(1,len(maze.node_dict)+1):
        #     print( maze.node_dict[i].get_index() )
        
        # bfs_path = maze.BFS( maze.get_start_point() )
        # for i in range(len(bfs_path)):
        #     print(bfs_path[i].get_index())
        # # print("=====================================")
        
        moving_list = maze.solveMaze()
        print(moving_list)
        
    elif mode == "2":
        bfs_2_path = maze.BFS_2( maze.get_node_dict()[1], maze.get_node_dict()[4] )
        bfs_2_path.append(maze.get_node_dict()[3])
        bfs_2_path.append(maze.get_node_dict()[5])
        bfs_2_path.append(maze.get_node_dict()[6])
        print(bfs_2_path)
        
        action_list = maze.getActions(bfs_2_path)
        print(action_list)
        print(maze.actions_to_str(action_list))
        
       
    else:
        log.error("Invalid mode")
        sys.exit(1)


if __name__ == "__main__":
    args = parse_args()
    main(**vars(args))
