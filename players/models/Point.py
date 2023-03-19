# from utils import unformat
import math


class Point:
    """A model of a 2-d cartesian coordinate Point."""
    x: float
    y: float
    STRING: str = "Point({x}, {y})"

    def __init__(self, x: float, y: float):
        """Construct a point with x, y coordinates."""
        self.x = x
        self.y = y

    # def __init__(self, string: str):
    #     """Construct a point from a string."""
    #     string = unformat(string, Point.STRING)
    #     if "x" in string:
    #         self.x = string["x"]
    #     else:
    #         raise ValueError("Unable to Find x coordinate")
    #     if "y" in string:
    #         self.y = string["y"]
    #     else:
    #         raise ValueError("Unable to Find y coordinate")

    def add(self, other):
        """Add two Point objects together and return a new Point."""
        self.x += other.x
        self.y += other.y
        return True

    def sub(self, other):
        """Add two Point objects together and return a new Point."""
        self.x -= other.x
        self.y -= other.y
        return True

    def distance(self, other) -> float:
        """Return the distance between two points."""
        x: float = self.x - other.x
        y: float = self.y - other.y
        return (x ** 2 + y ** 2) ** 0.5

    def make_unit_magnitude(self):
        """Return the unit vector of the point."""
        if self.distance(Point(0, 0)) == 0:
            return

        self.x = self.x / self.distance(Point(0, 0))
        self.y = self.y / self.distance(Point(0, 0))

    def get_angle(self) -> float:
        """Return the angle of the point."""
        if self.x == 0:
            if self.y == 0:
                return 0
            elif self.y > 0:
                return 90
            else:
                return 270
        elif self.x > 0:
            return math.degrees(math.atan(self.y / self.x))
        else:
            return math.degrees(math.atan(self.y / self.x)) + 180

    def __str__(self) -> str:
        """Return a string representation of the point."""
        return Point.STRING.format(x=self.x, y=self.y)

    def __repr__(self) -> str:
        """Return a string representation of the point."""
        return Point.STRING.format(x=self.x, y=self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
