import csv
import logging
import math
from enum import IntEnum
from typing import List

import numpy as np
import pandas

from node import Direction, Node

import queue

log = logging.getLogger(__name__)


class Action(IntEnum):
    ADVANCE = 1
    U_TURN = 2
    TURN_RIGHT = 3
    TURN_LEFT = 4
    HALT = 5


class Maze:
    def __init__(self, filepath: str):
        # TODO : read file and implement a data structure you like
        # For example, when parsing raw_data, you may create several Node objects.
        # Then you can store these objects into self.nodes.
        # Finally, add to nd_dict by {key(index): value(corresponding node)}
        self.raw_data = pandas.read_csv(filepath).to_numpy()
        self.clean_data = np.nan_to_num(self.raw_data,nan=0)
        self.clean_data = self.clean_data.astype(int)
        
        # print(self.clean_data)
        # print(len(self.clean_data))
        # print(self.clean_data[0][0])
        self.node_dict = dict()  # key: index, value: the correspond node
        for i in range (1,len(self.clean_data)+1):
            self.node_dict[i] = Node(i)
            
        for i in range(1, len(self.clean_data)+1):
            for j in range(1,5):
                if(self.clean_data[i-1][j] != 0):
                    self.node_dict[i].set_successor(  self.node_dict[ self.clean_data[i-1][j] ] ,Direction(j), self.clean_data[i-1][j+4])
                    
        # for i in range(1, len(self.node_dict)+1):
        #     print("Node", self.node_dict[i].get_index()) 
        #     for succ in self.node_dict[i].get_successors():
        #         print("Successor:", succ[0].get_index(), "Direction:", succ[1], "Distance:", succ[2])
            
            
            
    def get_start_point(self):
        if len(self.node_dict) < 2:
            log.error("Error: the start point is not included.")
            return 0
        return self.node_dict[1]
    
    def get_end_point(self):
        if len(self.node_dict) < 2:
            log.error("Error: the end point is not included.")
            return 0
        return self.node_dict[len(self.node_dict)]

    def get_node_dict(self):
        return self.node_dict

    def BFS(self, node: Node):
        # TODO : design your data structure here for your algorithm
        # Tips : return a sequence of nodes from the node to the nearest unexplored deadend
        goal_node = None
        q = queue.Queue()
        history = np.zeros(len(self.node_dict)+1) #record the history of nodes been thorugh, 0 for not been through, 1 for been through
        q.put(node)
        while not q.empty():
            cur = q.get()
            history[cur.get_index()] = 1
            for succ in cur.get_successors():
                if(history[ succ[0].get_index() ] != 1):
                    succ[0].set_parent(cur)
                    q.put(succ[0])
                    if(len(succ[0].get_successors()) == 1):
                        goal_node = succ[0]
                        q.queue.clear()
                        break
                        
        path = []
        while(goal_node != node):
            path.append(goal_node)
            goal_node = goal_node.get_parent()
        path.append(node)
        path.reverse()
        
        for i in range(1,len(self.node_dict)+1):
            self.node_dict[i].set_parent(None)

        return path

    def BFS_2(self, node_from: Node, node_to: Node):
        # TODO : similar to BFS but with fixed start point and end point
        # Tips : return a sequence of nodes of the shortest path
        q = queue.Queue()
        history = np.zeros(len(self.node_dict)+5) #record the history of nodes been thorugh, 0 for not been through, 1 for been through
        q.put(node_from)
        while not q.empty():
            cur = q.get()
            # print(cur.get_index())
            if(cur.get_index() == node_to.get_index()):
                break
            history[cur.get_index()] = 1
            for succ in cur.get_successors():
                # print("succ :",succ[0].get_index())
                if(history[ succ[0].get_index() ] != 1):
                    succ[0].set_parent(cur)
                    q.put(succ[0])
        path = []
        goal_node = node_to
        while(goal_node != node_from):
            # print(path)
            path.append(goal_node)
            goal_node = goal_node.get_parent()
        path.append(node_from)
        path.reverse()
        
        for i in range(1,len(self.node_dict)+1):
            self.node_dict[i].set_parent(None)

        return path

    def getAction(self, car_dir, node_from: Node, node_to: Node):
        # TODO : get the car action
        # Tips : return an action and the next direction of the car if the node_to is the Successor of node_to
        # If not, print error message and return 0
        if(node_from.is_successor(node_to)):
            match car_dir:
                case Direction.NORTH:
                    match node_from.get_direction(node_to):
                        case Direction.NORTH:
                            return Action.ADVANCE, Direction.NORTH
                        case Direction.SOUTH:
                            return Action.U_TURN, Direction.NORTH
                        case Direction.WEST:
                            return Action.TURN_LEFT, Direction.WEST
                        case Direction.EAST:
                            return Action.TURN_RIGHT, Direction.EAST
                case Direction.SOUTH:
                    match node_from.get_direction(node_to):
                        case Direction.NORTH:
                            return Action.U_TURN, Direction.SOUTH
                        case Direction.SOUTH:
                            return Action.ADVANCE, Direction.SOUTH
                        case Direction.WEST:
                            return Action.TURN_RIGHT, Direction.WEST
                        case Direction.EAST:
                            return Action.TURN_LEFT, Direction.EAST
                case Direction.WEST:
                    match node_from.get_direction(node_to):
                        case Direction.NORTH:
                            return Action.TURN_RIGHT, Direction.NORTH
                        case Direction.SOUTH:
                            return Action.TURN_LEFT, Direction.SOUTH
                        case Direction.WEST:
                            return Action.ADVANCE, Direction.WEST
                        case Direction.EAST:
                            return Action.U_TURN, Direction.WEST
                case Direction.EAST:
                    match node_from.get_direction(node_to):
                        case Direction.NORTH:
                            return Action.TURN_LEFT, Direction.NORTH
                        case Direction.SOUTH:
                            return Action.TURN_RIGHT, Direction.SOUTH
                        case Direction.WEST:
                            return Action.U_TURN, Direction.EAST
                        case Direction.EAST:
                            return Action.ADVANCE, Direction.EAST
        else:
            print(f"Node {node_to.get_index()} is not a successor of Node {node_from.get_index()}.")
            return 0

    def getActions(self, nodes: List[Node]):
        # TODO : given a sequence of nodes, return the corresponding action sequence
        # Tips : iterate through the nodes and use getAction() in each iteration
        action_list = []
        curr_node = nodes[0]
        car_dir = curr_node.get_direction(nodes[1])
        while(curr_node != nodes[-1]):
            action, car_dir = self.getAction(car_dir, curr_node, nodes[nodes.index(curr_node)+1])
            action_list.append(action)
            if(action == Action.ADVANCE):
                curr_node = nodes[nodes.index(curr_node)+1]
        return action_list

    def actions_to_str(self, actions):
        # cmds should be a string sequence like "fbrl....", use it as the input of BFS checklist #1
        cmd = "fbrls"
        cmds = ""
        # for action in actions:
        #     cmds += cmd[action - 1]
        i = 0
        while( i < len(actions)):
            if(actions[i] == Action.ADVANCE):
                cmds += "f"
            elif(actions[i] == Action.U_TURN and i < len(actions)-1 and actions[i+1] == Action.ADVANCE):
                cmds += "b"
                i = i + 1
            elif(actions[i] == Action.TURN_RIGHT and i < len(actions)-1 and actions[i+1] == Action.ADVANCE):
                cmds += "r"
                i = i + 1
            elif(actions[i] == Action.TURN_LEFT and i < len(actions)-1 and actions[i+1] == Action.ADVANCE):
                cmds += "l"
                i = i + 1
            elif(actions[i] == Action.HALT):
                cmds += "s"
            i = i + 1
        log.info(cmds)
        return cmds

    def strategy(self, node: Node):
        return self.BFS(node)

    def strategy_2(self, node_from: Node, node_to: Node):
        return self.BFS_2(node_from, node_to)
