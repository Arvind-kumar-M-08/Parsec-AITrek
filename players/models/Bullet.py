from .Point import Point
from .Obstacle import Obstacle
from .Agent import Agent
from constants import AGENT_RADIUS


class Bullet:
    _location: Point
    _direction: Point  # Only 8 directions possible and 0,0 is allowed for stop
    _energy: int
    _id: int
    STRING: str = "Bullet with id {id} at {location} with direction {direction} and energy {energy}"

    def __init__(self, location: Point, direction: Point, energy: int):
        self._location = location
        self._direction = direction
        self._energy = energy
        self._id = id(self)

    def get_direction(self) -> Point:
        return self._direction

    def get_energy(self) -> int:
        return self._energy

    def tick(self) -> None:
        if self._energy > 0:
            self._location.add(self._direction)
        else:
            return
        self._energy -= 1

    def is_alive(self) -> bool:
        return self._energy > 0

    def get_location(self) -> Point:
        return self._location

    def is_colliding_with_agent(self, agent: Agent) -> bool:
        """Given a bullet and agent check if they are colliding"""
        # if the obstacle is agent see if they are within some distance of the bullet.
        #  then make the bullet collide with them and make them and bullet die.
        distance = agent.get_location().distance(self.get_location())
        if distance < AGENT_RADIUS:
            # print("----------------------------")
            # print(self.get_location())
            # print(agent.get_location())
            # print(distance)
            # print(AGENT_RADIUS)
            return True
        else:
            return False

    def is_colliding_with_obstacle(self, obstacle: Obstacle) -> bool:
        return obstacle.checkInside(self.get_location())

    def is_colliding(self, obj: Obstacle or Agent) -> bool:
        """Given a bullet and obstacle check if they are colliding"""
        if isinstance(obj, Agent):
            return self.is_colliding_with_agent(obj)
        elif isinstance(obj, Obstacle):
            return self.is_colliding_with_obstacle(obj)

    def dead(self):
        self._energy = 0
