from __future__ import annotations
from typing import List
import time
from random import random, randint
from constants import *
from copy import deepcopy
from .Agent import Agent
from .Point import Point
from .Bullet import Bullet
from .Action import Action
from .Alert import Alert
from .ObjectSighting import ObjectSighting
from math import sin, cos, pi
from .State import State
from .Obstacle import Obstacle
from Generator import generate_obstacles_and_agents
from utils import isBetweenLineOfSight, is_point_in_vision, get_section_point, get_random_float

# from player_red import tick as player_red_tick
# from player_blue import tick as player_blue_tick
import socket
import pickle


class Environment:
    """The state of the environment."""

    agents: Dict[str, Dict[str, Agent]]
    bullets: List[Bullet]
    scores = Dict[str, int]
    n_invalid_actions: Dict[str, int]
    obstacles: List[Obstacle]
    time: int = 0
    alerts: Dict[str, List[Alert]]
    obstacles: List[Obstacle]
    _zone: List[Point]
    _safe_zone: List[Point]
    _is_zone_shrinking: bool = False
    _zone_shrink_times: List[int]
    # Choosing a random point in length/shrink_value of a side
    _shrink_value: int = SHRINK_VALUE
    _winner: str

    def __init__(self):
        """Initialize the cells with random locations and directions."""
        self.obstacles, circles = generate_obstacles_and_agents(
            NUMBER_OF_OBSTACLES, AGENTS_PER_TEAM << 1)
        self.agents = {"red": {}, "blue": {}}
        for i in range(len(circles)):
            if i % 2 == 0:
                self.agents["red"][str(i // 2)] = (
                    Agent(str(i // 2), Point(circles[i][0], circles[i][1]), Point(-1, 0), Point(1, 0), pi, "red"))
            else:
                self.agents["blue"][str(
                    i // 2)] = (Agent(str(i // 2), Point(circles[i][0], circles[i][1]), Point(-1, 0), Point(1, 0), pi, "blue"))

        self.bullets = []
        self.alerts = {
            "red": [],
            "blue": []
        }
        self.scores = {
            "red": 0,
            "blue": 0
        }
        self._zone = [Point(MAX_X, MAX_Y), Point(
            MAX_X, MIN_Y), Point(MIN_X, MIN_Y), Point(MIN_X, MAX_Y)]
        self.set_new_safe_zone()
        self._zone_shrink_times = [
            x * 5 for x in [100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 480]]
        self.n_invalid_actions = {
            "red": 0,
            "blue": 0
        }
        self._log = open("log.txt", "w")

        self.env_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.env_socket.bind((ENV_HOST, ENV_PORT))
        self.env_socket.settimeout(SOCKET_TIMEOUT)

    def tick(self) -> dict[int | str, int]:
        """Update the state of the simulation by one time step."""
        #  TODO: take a look at this

        if self.time % (UNIT_TIME / TICKS['Bullet']) == 0:
            for bullet in self.bullets:
                if bullet.is_alive():
                    self.enforce_bullet_collisions(bullet)
                    bullet.tick()
                else:
                    self.bullets.remove(bullet)

            self.enforce_zone()

        if self.time % (UNIT_TIME / TICKS['Agent']) == 0:
            for team in self.agents:
                for agent in self.agents[team].values():
                    agent.tick()
                    self.enforce_bounds(agent)
                    self.enforce_collisions(agent)
            red_state = self.generate_state('red')
            blue_state = self.generate_state('blue')

            red_state_serial = pickle.dumps(red_state)
            blue_state_serial = pickle.dumps(blue_state)

            try:
                while True:
                    self.env_socket.sendto(
                        blue_state_serial, (BLUE_HOST, BLUE_PORT))
                    blue_actions_serial, blue_addr = self.env_socket.recvfrom(
                        65527)
                    blue_actions = pickle.loads(blue_actions_serial)
                    if blue_addr[1] != BLUE_PORT:
                        continue
                    else:
                        break
            except Exception as e:
                # print("Blue Timeout:", e)
                blue_actions = []

            try:
                while True:
                    self.env_socket.sendto(
                        red_state_serial, (RED_HOST, RED_PORT))
                    red_actions_serial, red_addr = self.env_socket.recvfrom(
                        65527)
                    red_actions = pickle.loads(red_actions_serial)
                    if red_addr[1] != RED_PORT:
                        continue
                    else:
                        break
            except Exception as e:
                # print("Red Timeout:", e)
                red_actions = []

            # red_actions = player_red_tick(red_state)
            # blue_actions = player_blue_tick(blue_state)

            self.alerts['red'] = []
            self.alerts['blue'] = []

            validated_red_actions = self.validate_actions(red_actions, "red")
            validated_blue_actions = self.validate_actions(
                blue_actions, "blue")

            self.perform_actions(validated_red_actions, "red")
            self.perform_actions(validated_blue_actions, "blue")

            self.write_stats(red_state, blue_state, red_actions, blue_actions, validated_red_actions,
                             validated_blue_actions)

        self.caclulate_score()
        self.time += 1
        return {}

    def validate_actions(self, actions: List[Action], team: str) -> List[Action]:
        """Validate the actions of the agents."""
        validated_actions = []
        for action in actions:
            agent_id = str(action.agent_id)
            action_type = action.type
            action_direction = action.direction
            allowed = 0

            # check if action is on his agent only
            if agent_id in self.agents[team].keys():
                agent = self.agents[team][str(agent_id)]

                allowed = 1
                # - check if the agent is alive/dead
                if agent.get_health() == 0:
                    self.alerts[team].append(Alert(DEAD, agent_id))
                    allowed = 0
                    # raise Exception("Agent is already dead!")

                # - check if the agent is able to fire or not

                elif action_type == FIRE and not agent.can_fire():
                    self.alerts[team].append(Alert(FIRE_IMPOSSIBLE, agent_id))
                    allowed = 0

                # - make the direction's magnitude 1
                action_direction.make_unit_magnitude()

            else:
                self.alerts[team].append(Alert(WRONG_AGENT, agent_id))

            # Remove action if invalid and decrease the score based on that.
            if allowed == 0:
                self.n_invalid_actions[team] += 1
            else:
                validated_actions.append(action)

        return validated_actions

    def perform_actions(self, actions: List[Action], team: str):
        """Perform the actions of the agents."""
        for action in actions:
            agent_id = action.agent_id
            action_type = action.type
            action_direction = action.direction
            agent = self.agents[team][str(agent_id)]

            # IF ACTION ---> FIRE
            if action_type == FIRE:
                if agent.fire():
                    bullet_location = Point(
                        agent.get_location().x, agent.get_location().y)
                    offset = Point(1.5*AGENT_RADIUS*action_direction.x,
                                   1.5*AGENT_RADIUS*action_direction.y)
                    bullet_location.add(offset)
                    self.bullets.append(
                        Bullet(bullet_location, action_direction, INITIAL_BULLET_ENERGY))

            # UPDATE DIRECTION
            if action_type == UPDATE_DIRECTION:
                agent.set_direction(action_direction)

            # UPDATE VIEW DIRECTION
            if action_type == UPDATE_VIEW_DIRECTION:
                agent.set_view_direction(action_direction)

    def write_stats(self, red_state: State, blue_state: State, red_actions: List[Action], blue_actions: List[Action],
                    validated_red_actions: List[Action], validated_blue_actions: List[Action]) -> None:
        """Write the stats of the simulation to a file."""
        self._log.write(f"Game time: {self.time} Real Time: {time.time()}\n")
        self._log.write(f"STARTING GAME LOG FOR TIME {self.time}\n")
        self._log.write(f"Red Agents: {len(self.agents['red'])} Red Score: {self.scores['red']} "
                        f"|| Blue Agents: {len(self.agents['blue'])} Blue Score: {self.scores['blue']}\n")
        # log map elements
        self._log.write("STARTING LOG OF MAP ELEMENTS\n")

        self._log.write("LOGGING AGENTS\n")
        for team in self.agents:
            for agent in self.agents[team].values():
                self._log.write(f"{agent}\n")

        self._log.write("LOGGING BULLETS\n")
        for bullet in self.bullets:
            self._log.write(f"{bullet}\n")

        self._log.write("ENDING LOG OF MAP ELEMENTS\n")

        self._log.write("STARTING LOG OF STATES\n")

        self._log.write("LOGGING RED STATE\n")
        self._log.write(f"{red_state}\n")

        self._log.write("LOGGING BLUE STATE\n")
        self._log.write(f"{blue_state}\n")

        self._log.write("ENDING LOG OF STATES\n")

        self._log.write("STARTING LOG OF ACTIONS\n")

        self._log.write("LOGGING RED ACTIONS\n")
        for action in red_actions:
            self._log.write(f"  {action}\n")

        self._log.write("LOGGING BLUE ACTIONS\n")
        for action in blue_actions:
            self._log.write(f"  {action}\n")

        self._log.write("ENDING LOG OF ACTIONS\n")

        self._log.write("STARTING LOG OF VALIDATED ACTIONS\n")

        self._log.write("LOGGING RED VALIDATED ACTIONS\n")
        for action in validated_red_actions:
            self._log.write(f"  {action}\n")

        self._log.write("LOGGING BLUE VALIDATED ACTIONS\n")
        for action in validated_blue_actions:
            self._log.write(f"  {action}\n")

        self._log.write("ENDING LOG OF VALIDATED ACTIONS\n")

        self._log.write("STARTING LOG OF ALERTS\n")

        self._log.write("LOGGING RED ALERTS\n")
        for alert in self.alerts['red']:
            self._log.write(f"{alert}\n")

        self._log.write("LOGGING BLUE ALERTS\n")
        for alert in self.alerts['blue']:
            self._log.write(f"{alert}\n")

        self._log.write("ENDING LOG OF ALERTS\n")

        self._log.write(f"ENDING GAME LOG FOR TIME {self.time}\n")

    def generate_state(self, team: str) -> State:
        """Generate the state of the environment."""

        agents = self.agents[team]
        object_in_sight = {}

        for agent in agents:
            object_in_sight[agent] = self.get_object_in_sight(agents[agent])

        return deepcopy(State(agents, object_in_sight, self.alerts[team], team, self.time, self.obstacles, self._zone,
                              self._safe_zone, self._is_zone_shrinking))

    def get_object_in_sight(self, agent: Agent) -> Dict[str, List[ObjectSighting]]:

        object_in_sight = []
        non_blocked_object_in_sight = []

        # opponent's agents
        for team in self.agents:
            if team != agent.get_team():
                for opponent_agent in self.agents[team].values():
                    if opponent_agent.is_alive() and is_point_in_vision(agent, opponent_agent.get_location(), opponent_agent.get_radius()):
                        object_in_sight.append(ObjectSighting(OPPONENT, opponent_agent.get_location(),
                                                              opponent_agent.get_direction()))

        # bullets
        for bullet in self.bullets:
            if is_point_in_vision(agent, bullet.get_location(), 0):
                object_in_sight.append(ObjectSighting(
                    BULLET, bullet.get_location(), bullet.get_direction()))

        # checking if the line of sight passes through a wall
        for _object in object_in_sight:
            blocked = False
            for obstacle in self.obstacles:
                if isBetweenLineOfSight(agent.get_location(), _object.location, obstacle.corners):
                    blocked = True
                    break
            if not blocked:
                non_blocked_object_in_sight.append(_object)

        agents, bullets = [], []
        for non_blocking_object in non_blocked_object_in_sight:
            if non_blocking_object.object_type == OPPONENT:
                agents.append(non_blocking_object)
            else:
                bullets.append(non_blocking_object)

        return {
            "Agents": agents,
            "Bullets": bullets
        }

    @staticmethod
    def random_location() -> Point:
        # TODO: make this more random
        return Point(randint(int(MIN_X), int(MAX_X)), randint(int(MIN_Y), int(MAX_Y)))

    @staticmethod
    def random_direction() -> Point:
        """Generate a 'point' used as a directional vector."""
        angle = random() * 2.0 * pi
        x = cos(angle)
        y = sin(angle)
        return Point(x, y)

    def enforce_bounds(self, agent: Agent) -> None:
        """Cause a cell to 'bounce' if it goes out of bounds."""
        is_alert = False
        if agent.get_location().x + AGENT_RADIUS > MAX_X:
            agent.set_location(
                Point(MAX_X - AGENT_RADIUS, agent.get_location().y))
            is_alert = True

        if agent.get_location().x - AGENT_RADIUS < MIN_X:
            agent.set_location(
                Point(MIN_X + AGENT_RADIUS, agent.get_location().y))
            is_alert = True

        if agent.get_location().y + AGENT_RADIUS > MAX_Y:
            agent.set_location(
                Point(agent.get_location().x, MAX_Y - AGENT_RADIUS))
            is_alert = True
        if agent.get_location().y - AGENT_RADIUS < MIN_Y:
            agent.set_location(
                Point(agent.get_location().x, MIN_Y + AGENT_RADIUS))
            is_alert = True

        if is_alert:
            self.alerts[agent.get_team()].append(
                Alert(COLLISION, agent.agent_id))

    def enforce_collisions(self, agent: Agent) -> None:
        """Cause an agent to stop if it collides with another agent."""
        # - check if the agent is alive/dead
        # - check if it collided with a wall, agent
        # - else stop the agent.
        #

        # Checking whether the agent is alive or not
        agent_alive = agent.get_health() > 0
        if not agent_alive:
            agent.stop()
            return

        # Checking agent-obstacle collision
        for obstacle in self.obstacles:
            if obstacle.intersects_circle(agent.get_location() + agent.get_direction(), AGENT_RADIUS):
                # agent.stop()
                agent.get_location().sub(agent.get_direction())
                self.alerts[agent.get_team()].append(
                    Alert(COLLISION, agent.agent_id))

                break

        # Checking agent-agent collision
        for team in self.agents:
            for other_agent in self.agents[team].values():
                if agent != other_agent:
                    if not other_agent.is_alive():
                        continue
                    agent_collision = (agent.get_direction() + agent.get_location()).distance(
                        other_agent.get_location() + other_agent.get_direction()) <= 2 * AGENT_RADIUS
                    if agent_collision:
                        # agent.stop()
                        agent.get_location().sub(agent.get_direction())
                        self.alerts[agent.get_team()].append(
                            Alert(COLLISION, agent.agent_id))
                    break

        return

    def enforce_bullet_collisions(self, bullet: Bullet) -> None:
        """Cause a bullet to stop if it collides with another agent or obstacle."""
        # check collision with zone
        zone_obstacle = Obstacle([point for point in self._zone])
        if not zone_obstacle.checkInside(bullet.get_location()):
            bullet.dead()
            self.bullets.remove(bullet)
            return

        for obstacle in self.obstacles:
            if bullet.is_colliding(obstacle):
                bullet.dead()
                self.bullets.remove(bullet)
                return

        for team in self.agents:
            for agent in self.agents[team].values():
                if bullet.is_colliding(agent):
                    bullet.dead()
                    self.bullets.remove(bullet)
                    agent.decrease_health(BULLET_HIT)
                    return

    def decrease_agent_health(self, bullet: Bullet, agent):
        """Decrease the heath of agent depending on the energy of bullet"""
        # TODO: find an appropriate formula for health deduction.
        pass

    def enforce_zone(self):
        # Setting is_zone_shrinking to false
        self._is_zone_shrinking = False
        i = 0
        zone_shrink_times_len = len(self._zone_shrink_times)
        while i < zone_shrink_times_len - 1:
            if self._zone_shrink_times[i] <= self.time <= self._zone_shrink_times[i] + (
                    self._zone_shrink_times[i + 1] - self._zone_shrink_times[i]) // 2:
                self._is_zone_shrinking = True
                break
            i += 1

        # Final Shrink
        if self._zone_shrink_times[zone_shrink_times_len - 2] <= self.time <= self._zone_shrink_times[
                zone_shrink_times_len - 1]:
            self._is_zone_shrinking = True
            time_left = self._zone_shrink_times[zone_shrink_times_len - 1] - self.time
            self.shrink_zone(time_left)

        # Shrinking zone
        elif self._is_zone_shrinking:
            time_to_stop_shrinking = self._zone_shrink_times[i] + (
                self._zone_shrink_times[i + 1] - self._zone_shrink_times[i]) // 2
            time_left = time_to_stop_shrinking - self.time

            # Shrinking the zone
            self.shrink_zone(time_left)

            # Shrinking complete and choose new safe zone
            if time_left == 0:
                if i < len(self._zone_shrink_times) - 3:
                    self.set_new_safe_zone()
                    self._is_zone_shrinking = False
                else:
                    # setting final zone
                    self.set_final_zone()

        # Impose zone penalty
        self.enforce_zone_penalty()

    def set_final_zone(self):
        final_x = (self._safe_zone[0].x + self._safe_zone[3].x) / 2
        final_y = (self._safe_zone[0].y + self._safe_zone[1].y) / 2
        directions = [1, 1, -1, -1]
        for i in range(4):
            point = Point(
                final_x + directions[i] * FINAL_SIZE, final_y + directions[(i + 1) % 4] * FINAL_SIZE)
            self._safe_zone[i] = point

    def shrink_zone(self, time_left: int):
        new_zone = []
        for i in range(len(self._zone)):
            new_zone.append(get_section_point(
                self._zone[i], self._safe_zone[i], 1, time_left))

        # Setting zone after shrinking
        self._zone = new_zone

    def set_new_safe_zone(self):

        # Convention for zone and  safe-zone 0 -> top-right then clockwise
        # (x1, y1) left-top corner of the new zone
        # (x2, y2) right-bottom corner of the new zone
        x1 = get_random_float(self._zone[3].x,
                              get_section_point(self._zone[3], self._zone[0], 1, self._shrink_value - 1).x)
        y1 = get_random_float(get_section_point(self._zone[3], self._zone[2], 1, self._shrink_value - 1).y,
                              self._zone[3].y)
        x2 = get_random_float(get_section_point(self._zone[1], self._zone[2], 1, self._shrink_value - 1).x,
                              self._zone[1].x)
        y2 = get_random_float(self._zone[1].y,
                              get_section_point(self._zone[1], self._zone[0], 1, self._shrink_value - 1).y)

        self._safe_zone = [Point(x2, y1), Point(
            x2, y2), Point(x1, y2), Point(x1, y1)]

    def enforce_zone_penalty(self):
        # Reducing agents' health outside the zone
        # Considering zone as a obstacle polygon for checkInside function reuse
        zone_obstacle = Obstacle([point for point in self._zone])
        for team in self.agents:
            for agent in self.agents[team].values():
                if not zone_obstacle.checkInside(agent.get_location()):
                    agent.decrease_health(OUTSIDE_ZONE)

    def is_all_dead(self, team: str) -> bool:
        for agent in self.agents[team].values():
            if agent.is_alive():
                return False
        return True

    def is_complete(self) -> bool:
        """Method to indicate when the simulation is complete."""
        # TODO: implement this
        is_red_dead = self.is_all_dead("red")
        is_blue_dead = self.is_all_dead("blue")

        if is_blue_dead and is_red_dead:
            # need to see score here

            self._winner = "draw"
        elif is_blue_dead:
            self._winner = "red"
        elif is_red_dead:
            self._winner = "blue"
        else:
            return False

        return True

        # we don't need this as this can be controlled using shrink times
        if self.time > MAX_TIME:
            return True
        return False

    def get_winner(self):
        return self._winner

    def get_current_zone(self):
        return self._zone

    def get_current_safe_zone(self):
        return self._safe_zone

    def caclulate_score(self):
        """Calculate the score for each team"""
        opposite_team = {"red": "blue", "blue": "red"}

        for team in self.scores:
            self.scores[team] = 0
            for agent_id, agent in self.agents[opposite_team[team]].items():
                self.scores[team] += INITIAL_AGENT_HEALTH - agent.get_health()
