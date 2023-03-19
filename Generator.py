from models.Obstacle import Obstacle
from models.Point import Point
from constants import *
import random
import math


def generate_random_circles(N):
    map_area = (MAX_X - MIN_X) * (MAX_Y - MIN_Y)
    circle_area = map_area * OBSTACLE_PERCENTAGE / N
    circles = []
    i = 0
    while i < N:

        radius = math.sqrt(circle_area / math.pi)
        x = random.uniform(MIN_X + radius, MAX_X - radius)
        y = random.uniform(MIN_Y + radius, MAX_Y - radius)
        intersects = False
        for circle in circles:
            distance = math.sqrt((x - circle[0]) ** 2 + (y - circle[1]) ** 2)
            if distance < radius + circle[2]:
                intersects = True
                break

        if not intersects:
            circles.append((x, y, radius))
            i += 1

    return circles


def get_points_on_circle(circle, number_of_points):
    points = []
    radian_hash = {}
    for i in range(number_of_points):
        total_angle = 2 * math.pi
        theta = random.uniform(
            i * total_angle / number_of_points, (i + 1) * total_angle / number_of_points)
        point = Point(circle[0] + circle[2] * math.cos(theta),
                      circle[1] + circle[2] * math.sin(theta))
        radian_hash[str(point)] = theta
        points.append(point)
    points.sort(key=lambda point: radian_hash[str(point)])
    return points


def generate_obstacles_and_agents(number_of_obstacles, n):
    # TODO: Generate non intersecting polygon obstacles
    obstacles = []
    distinct_circles = generate_random_circles(number_of_obstacles+n)
    # print(len(distinct_circles))
    for circle in distinct_circles[:number_of_obstacles]:
        number_of_points = random.randint(
            MIN_OBSTACLE_SIDES, MAX_OBSTACLE_SIDES)
        obstacle_corners = get_points_on_circle(circle, number_of_points)
        obstacle = Obstacle(obstacle_corners)
        obstacles.append(obstacle)
    # print(distinct_circles)
    return obstacles, distinct_circles[number_of_obstacles:]
