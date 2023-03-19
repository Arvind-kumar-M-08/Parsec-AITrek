from .Point import Point
from .Line import Line
from typing import List
from shapely.geometry import Polygon
from shapely.geometry import Point as ShapelyPoint


class Obstacle:
    corners: List[Point]
    n: int  # No of Corners
    STRING: str = "Obstacle with {n} corners at {corners}"

    # Only Polygon Obstacles are allowed
    def __init__(self, corners: List[Point]):
        self.corners = corners
        self.n = len(corners)

    def __str__(self):
        return self.STRING.format(corners=self.corners, n=self.n)

    def __repr__(self):
        return self.STRING.format(corners=self.corners, n=self.n)

    def intersects_circle(self, center: Point, radius: float) -> bool:
        circle = ShapelyPoint(center.x, center.y).buffer(radius)
        poly = Polygon([[p.x, p.y] for p in self.corners])
        return poly.intersects(circle)
    
    def checkInside(self, p: Point):
        # When polygon has less than 3 edge, it is not polygon
        if self.n < 3:
            return False

        # Create a point at infinity, y is same as point p
        ext_line = Line(p, Point(9999, p.y))
        count = 0
        i = 0
        while True:
            # Forming a line from two consecutive points of poly
            side = Line(self.corners[i], self.corners[(i + 1) % self.n])
            if ext_line.isIntersect(side):
                # If side is intersects ex
                if Line.direction(side.p1, p, side.p2) == 0:
                    return side.onLine(p)
                count += 1

            i = (i + 1) % self.n
            if i == 0:
                break

        # When count is odd
        return count & 1

    def get_edges(self) -> List[Line]:
        edges = []
        for i in range(self.n):
            edges.append(Line(self.corners[i], self.corners[(i + 1) % self.n]))
        return edges
