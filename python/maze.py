import csv
import logging
import math
from enum import IntEnum
from typing import List
from itertools import permutations
import time

import numpy as np
import pandas

from node import Direction, Node

import queue

log = logging.getLogger(__name__)


class Action(IntEnum):
    START = 0
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

        self.t = {}
        self.t['f'] = 1
        self.t['b'] = 2
        self.t['r'] = 1.5
        self.t['l'] = 1.5
        self.t['s'] = 0          
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
                            return Action.U_TURN, Direction.SOUTH
                        case Direction.WEST:
                            return Action.TURN_LEFT, Direction.WEST
                        case Direction.EAST:
                            return Action.TURN_RIGHT, Direction.EAST
                case Direction.SOUTH:
                    match node_from.get_direction(node_to):
                        case Direction.NORTH:
                            return Action.U_TURN, Direction.NORTH
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
                            return Action.U_TURN, Direction.EAST
                case Direction.EAST:
                    match node_from.get_direction(node_to):
                        case Direction.NORTH:
                            return Action.TURN_LEFT, Direction.NORTH
                        case Direction.SOUTH:
                            return Action.TURN_RIGHT, Direction.SOUTH
                        case Direction.WEST:
                            return Action.U_TURN, Direction.WEST
                        case Direction.EAST:
                            return Action.ADVANCE, Direction.EAST
        else:
            print(f"Node {node_to.get_index()} is not a successor of Node {node_from.get_index()}.")
            return 0

    def getActions(self, nodes: List[Node]):
        # TODO : given a sequence of nodes, return the corresponding action sequence
        # Tips : iterate through the nodes and use getAction() in each iteration
        # print(nodes)
        # for i in range(len(nodes)):
        #     print(nodes[i].get_index(), end=' ')
        # print()
        action_list = []
        
        curr_node_index = 0
        curr_node = nodes[0]
        car_dir = curr_node.get_direction(nodes[1])
        while(curr_node_index < len(nodes)-1):
            action, car_dir = self.getAction(car_dir, nodes[curr_node_index], nodes[curr_node_index+1])
            action_list.append(action)
            if(action == Action.ADVANCE):
                curr_node_index += 1
            # print(f"Action: {action}, Direction: {car_dir}")
            # print(curr_node.get_index(), nodes[nodes.index(curr_node)+1].get_index(), end='\n')
            # print(action_list)
            # time.sleep(1)
        return  self.actions_to_actions(action_list)

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
        # log.info(cmds)
        return cmds
    def actions_to_char(self, actions):
        # cmd = "fbrls"
        cmds = []
        for action in actions:
            if action == Action.ADVANCE:
                cmds.append("f")
            elif action == Action.U_TURN:
                cmds.append("b")
            elif action == Action.TURN_RIGHT:
                cmds.append("r")
            elif action == Action.TURN_LEFT:
                cmds.append("l")
            elif action == Action.HALT:
                cmds.append("s")
        return cmds

    def actions_to_actions(self, actions):
        cmds = []
        i = 0
        while( i < len(actions)):
            if(actions[i] == Action.ADVANCE):
                cmds.append(Action.ADVANCE)
            elif(actions[i] == Action.U_TURN and i < len(actions)-1 and actions[i+1] == Action.ADVANCE):
                cmds.append(Action.U_TURN)
                i = i + 1
            elif(actions[i] == Action.TURN_RIGHT and i < len(actions)-1 and actions[i+1] == Action.ADVANCE):
                cmds.append(Action.TURN_RIGHT)
                i = i + 1
            elif(actions[i] == Action.TURN_LEFT and i < len(actions)-1 and actions[i+1] == Action.ADVANCE):
                cmds.append(Action.TURN_LEFT)
                i = i + 1
            elif(actions[i] == Action.HALT):
                cmds.append(Action.HALT)
            i = i + 1
        return cmds


    def findRoot(self):
        roots = []
        for node in self.node_dict.values():
            if len(node.get_successors()) == 1:
                roots.append(node)
        return roots
    
    def all_permutations(self, roots):
        # print(roots)
        perm = permutations(roots)
        return list(perm)
    
    def getDis(self):
        n = len(self.node_dict)
        dis = [[0 for x in range(n)] for y in range(n)]
        for i in range(1, n+1):
            for j in range(1, n+1):
                if i == j: continue
                path = self.BFS_2(self.node_dict[i], self.node_dict[j])
                action = self.actions_to_char(self.getActions(path))
                # print(path, self.getActions(path))
                temp_dis = 0
                # print(i, j, end=' ')
                for k in action:
                    # print(k, end=' ')
                    temp_dis += self.t[k] 
                # print()
                dis[i-1][j-1] = temp_dis
        return dis
    
    def solveMaze(self):
        roots = self.findRoot()
        start = roots[0]
        end = roots[-1]
        dis = self.getDis()
        all_perm = self.all_permutations(roots)
        # print(dis)
        min_dis = math.inf
        min_path = []
        for perm in all_perm:
            if perm[0] != start or perm[-1] != end:
                continue
            path = [start]
            for root in perm:
                path += self.BFS_2(path[-1], root)[1:]
            total_dis = 0
            for i in range(len(path)-1):
                total_dis += dis[path[i].get_index()-1][path[i+1].get_index()-1]

                # one must u turn from a root to another
                if path[i] in roots:
                    total_dis += self.t['b']
            if total_dis < min_dis:
                min_dis = total_dis
                min_path = path
        
        # print(min_dis)
        for i in min_path:
            print(i.get_index(), end=' ')
        print()
        actions = self.getActions(min_path)
        # cmds = self.actions_to_str(actions)
        # print(actions)
        actions.insert(0,Action.START)
        actions.append(Action.HALT)
        actions_str = self.actions_to_char(actions)
        res = 0
        for i in actions_str:
            res += self.t[i]
        print(f"total distant: {res}")
        return actions
    
    def solveMaze_2(self):
        roots = self.findRoot()
        start = roots[0]
        end = roots[-1]
        dis = self.getDis()
        n = len(roots)
        idx = {}
        for i in range(n):
            # print(roots[i].get_index(), end=' ')
            idx[roots[i].get_index()] = i
        # print()
        # print(idx)
        dp = [[math.inf for x in range(1 << n)] for y in range(n)]
        dp[idx[start.get_index()]][1 << (idx[start.get_index()])] = 0
        par = [[-1 for x in range(1 << n)] for y in range(n)]

        # print(dis)
        for mask in range (2,1 << n):
            for j in range (0, n):
                if not (mask & (1 << j)):
                    continue
                for i in range (1,n):
                    # (list(mydict.keys())[list(mydict.values()).index(16)])
                    x = (list(idx.keys())[list(idx.values()).index(i)])
                    y = (list(idx.keys())[list(idx.values()).index(j)])
                    temp = dp[j][mask ^ (1 << i)] + dis[x-1][y-1]
                    if temp < dp[i][mask]:
                        dp[i][mask] = temp
                        par[i][mask] = j

        cur_node_idx = idx[end.get_index()]
        mask = (1 << n) - 1
        path = []
        # for i in range(n):
        #     print(i)
        #     for mask in range(1 << n):
        #         print(bin(mask), dp[i][mask])
        # print(len(par))
        while cur_node_idx != -1:
            cur_node = (list(idx.keys())[list(idx.values()).index(cur_node_idx)])
            # print(cur_node, cur_node_idx, bin(mask))
            path.append(cur_node)
            temp = par[cur_node_idx][mask]
            # print(cur_node_idx)
            if cur_node_idx != -1:
                mask ^= (1 << (cur_node_idx))
                cur_node_idx = temp

        path.reverse()
        # print(path)
        path_node = [start]
        for i in range(1, len(path)):
            path_node += self.BFS_2(path_node[-1], self.node_dict[path[i]])[1:]
        for i in path_node:
            print(i.get_index(), end=' ')
        print()
        actions = self.getActions(path_node)
        actions.insert(0,Action.START)
        actions.append(Action.HALT)
        actions_str = self.actions_to_char(actions)
        res = 0
        for i in actions_str:
            res += self.t[i]
        print(f"total distant: {res}")
        return actions
        
    def strategy(self, node: Node):
        return self.BFS(node)

    def strategy_2(self, node_from: Node, node_to: Node):
        return self.BFS_2(node_from, node_to)
