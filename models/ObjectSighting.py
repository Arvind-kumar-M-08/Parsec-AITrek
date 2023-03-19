from .Point import Point
from constants import WALL, BULLET, OPPONENT


class ObjectSighting:
    object_type: str  # Opponent's Agent, Bullet
    location: Point
    direction: Point  # For Wall it's Point(0,0)
    _id: int
    STRING: str = "ObjectSighting with id {id} of type {object_type} at {location} with direction {direction}"

    def __init__(self, object_type: str, location: Point, direction: Point):
        self.object_type = object_type
        self.location = location
        if object_type == WALL:
            self.direction = Point(0, 0)
        else:
            self.direction = direction

        self._id = id(self)

    def get_location(self):
        return self.location
    
    def get_direction(self):
        return self.direction
    
    def __str__(self):
        return ObjectSighting.STRING.format(object_type=self.object_type, location=self.location, direction=self.direction, id=self._id)

    def __repr__(self):
        return ObjectSighting.STRING.format(object_type=self.object_type, location=self.location, direction=self.direction, id=self._id)
