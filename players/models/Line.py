from .Point import Point


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return "Line from {p1} to {p2}".format(p1=self.p1, p2=self.p2)

    def __repr__(self):
        return "Line from {p1} to {p2}".format(p1=self.p1, p2=self.p2)

    def onLine(self, p: Point):
        # check if the point is on the line.
        if (
                p.x <= max(self.p1.x, self.p2.x)
                and p.x <= min(self.p1.x, self.p2.x)
                and (p.y <= max(self.p1.y, self.p2.y) and p.y <= min(self.p1.y, self.p2.y))
        ):
            return True
        return False

    @staticmethod
    def direction(a: Point, b: Point, c: Point):
        val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
        if val == 0:
            # Collinear
            return 0
        elif val < 0:
            # Anti-clockwise direction
            return 2
        # Clockwise direction
        return 1

    def isIntersect(self, l2):
        # Four direction for two lines and points of other line
        dir1 = self.direction(self.p1, self.p2, l2.p1)
        dir2 = self.direction(self.p1, self.p2, l2.p2)
        dir3 = self.direction(l2.p1, l2.p2, self.p1)
        dir4 = self.direction(l2.p1, l2.p2, self.p2)

        # When intersecting
        if dir1 != dir2 and dir3 != dir4:
            return True

        # When p2 of line2 are on the line1
        if dir1 == 0 and self.onLine(l2.p1):
            return True

        # When p1 of line2 are on the line1
        if dir2 == 0 and self.onLine(l2.p2):
            return True

        # When p2 of line1 are on the line2
        if dir3 == 0 and l2.onLine(self.p1):
            return True

        # When p1 of line1 are on the line2
        if dir4 == 0 and l2.onLine(self.p2):
            return True

        return False
