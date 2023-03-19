## THIS IS A RANDOM BOT

from models.State import State
from models.Action import Action
from models.Point import Point
from models.Obstacle import Obstacle
from constants import *
import random
import math
from typing import List
import socket
import pickle
import sys


#     agents: Dict[str, Agent]  # The player's agents
#     object_in_sight: Dict[str, List[ObjectSighting]]  # Agent : [ObjectSighting] ,Bullet: [ObjectSighting]  ,Wall: [
#     # ObjectSighting]
#     Alerts: List[Alert]  # List of alerts collisions, zone, bullet_hit etc
#     team: str
#     time: int
#     obstacles: List[Obstacle]  # List of obstacles in the environment
#     zone: List[Point]  # List of corners in the zone
#     safe_zone: List[Point]  # List of corners in the safe zone
#     is_zone_shrinking: bool  # True if zone is shrinking, False if zone is expanding
#     STRING = "Agents: {agents} \n Object in sight: {object_in_sight} \n Alerts: {alerts} \n Team: {team} \n Time: {" \
#              "time} \n Obstacles: {obstacles} \n Zone: {zone} \n Safe Zone: {safe_zone} \n Is Zone Shrinking: {" \
#              "is_zone_shrinking} "



def tick(state: State) -> List[Action]:

    actions = []
    for agent_id in state.agents: 
        flag = 0 # flag to check if we have given an action
        agent = state.agents[agent_id]

        for alert in state.alerts:
            if alert.alert_type == COLLISION: # if collision with wall, update to opposite direction
                type = UPDATE_DIRECTION
                direction = Point(agent.get_direction().x,
                                  agent.get_direction().y) + Point(random.uniform(-3, 3), random.uniform(-3, 3))

                action = Action(agent_id, type, direction) # create action
                flag = 1
                break

        if flag == 0:
            rand_val = random.uniform(0, 1)
            # print(rand_val)
            if rand_val < 0.3: # 30% chance to update view direction
                type = UPDATE_VIEW_DIRECTION
                current_direction = agent.get_view_direction()
                direction = current_direction + \
                    Point(random.uniform(-1, 1), random.uniform(-1, 1))
            elif rand_val < 0.8: # 50% chance to update direction
                type = UPDATE_DIRECTION
                current_direction = agent.get_direction()
                direction = current_direction + \
                    Point(random.uniform(-1, 1), random.uniform(-1, 1))
            else: # 20% chance to fire
                type = FIRE
                direction = Point(random.uniform(-1, 1), random.uniform(-1, 1))

        action = Action(agent_id, type, direction)
        actions.append(action)

    # return the actions of all the agents
    return actions



if __name__ == '__main__':
    server_port = ENV_PORT
    server_host = ENV_HOST

    red_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    red_socket.settimeout(2)

    red_host = 'localhost'
    red_port = RED_PORT
    red_socket.bind((red_host, red_port))

    print("Red player is ready to receive messages...")
    while True:
        try:
            environment_message, addr = red_socket.recvfrom(65527)
        except:
            print("Environment Not Responding...Red Closed")
            red_socket.close()
            sys.exit(1)
        state = pickle.loads(environment_message)
        actions = tick(state)
        new_message = pickle.dumps(actions)
        red_socket.sendto(new_message, (server_host, server_port))
