from .Agent import Agent
from typing import Dict, List
from .Alert import Alert
from .Obstacle import Obstacle
from .Point import Point
from .ObjectSighting import ObjectSighting


class State:
    agents: Dict[str, Agent]  # The player's agents
    object_in_sight: Dict[str, List[ObjectSighting]]  # Agent : [ObjectSighting] ,Bullet: [ObjectSighting]
    Alerts: List[Alert]  # List of alerts collisions, zone, bullet_hit etc
    team: str
    time: int
    obstacles: List[Obstacle]  # List of obstacles in the environment
    zone: List[Point]  # List of corners in the zone
    safe_zone: List[Point]  # List of corners in the safe zone
    is_zone_shrinking: bool  # True if zone is shrinking, False otherwise.
    STRING = "Agents: {agents} \n Object in sight: {object_in_sight} \n Alerts: {alerts} \n Team: {team} \n Time: {" \
             "time} \n Obstacles: {obstacles} \n Zone: {zone} \n Safe Zone: {safe_zone} \n Is Zone Shrinking: {" \
             "is_zone_shrinking} "

    def __init__(self, agents: Dict[str, Agent], object_in_sight: Dict[str, List], alerts: List[Alert], team: str, time: int, obstacles: List[Obstacle], zone: List[Point], safe_zone: List[Point], is_zone_shrinking: bool):
        self.agents = agents
        self.object_in_sight = object_in_sight
        self.alerts = alerts
        self.team = team
        self.time = time
        self.obstacles = obstacles
        self.zone = zone
        self.safe_zone = safe_zone
        self.is_zone_shrinking = is_zone_shrinking

    def __str__(self):
        return self.STRING.format(agents=self.agents, object_in_sight=self.object_in_sight, alerts=self.alerts, team=self.team, time=self.time, obstacles=self.obstacles, zone=self.zone, safe_zone=self.safe_zone, is_zone_shrinking=self.is_zone_shrinking)

    def __repr__(self):
        return self.STRING.format(agents=self.agents, object_in_sight=self.object_in_sight, alerts=self.alerts, team=self.team, time=self.time, obstacles=self.obstacles, zone=self.zone, safe_zone=self.safe_zone, is_zone_shrinking=self.is_zone_shrinking)





