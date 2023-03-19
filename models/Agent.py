from .Point import Point
from constants import *
from constants import DAMAGES


class Agent:
    """A model of a cell agent."""
    AGENT_RADIUS: int = AGENT_RADIUS  # Radius of the agent
    _location: Point  # current location of the agent
    _direction: Point  # angle in which the agent is going

    _range: float  # range of the agent's view
    _view_angle: float

    _view_direction: Point  # angle in which the agent is facing
    _fire_time: int  # time until the agent can fire again

    _health: int = INITIAL_AGENT_HEALTH  # health of the agent

    _team: str
    _id: int
    agent_id: str

    STRING: str = "Agent with id {id} at {location} and direction {direction} and view direction {view_direction} and" \
                  " health {health} and fire time {fire_time} and team {team} and range {range} and view angle {" \
                  "view_angle}"

    def __init__(self, agent_id: str, location: Point, direction: Point, view_direction: Point, view_angle: float,
                 team: str, view_range: float = AGENT_VIEW_RANGE):
        """Construct an agent with location, velocity, radius, color, and id."""
        self._location = location
        self._direction = direction  # only 8 directions possible and 0,0 is allowed for stop
        self._range = view_range
        self._view_angle = view_angle
        self._view_direction = view_direction
        self._health = INITIAL_AGENT_HEALTH
        self._team = team
        self._id = id(self)
        self.agent_id = agent_id
        self._fire_time = 0

    def __str__(self) -> str:
        """Return a string representation of the agent."""
        return Agent.STRING.format(id=self._id, location=self._location, direction=self._direction,
                                   view_direction=self._view_direction, health=self._health, fire_time=self._fire_time,
                                   team=self._team, range=self._range, view_angle=self._view_angle)

    def __repr__(self) -> str:
        """Return a string representation of the agent."""
        return Agent.STRING.format(id=self._id, location=self._location, direction=self._direction,
                                   view_direction=self._view_direction, health=self._health, fire_time=self._fire_time,
                                   team=self._team, range=self._range, view_angle=self._view_angle)

    def get_location(self) -> Point:
        return self._location

    def get_direction(self) -> Point:
        return self._direction

    def set_direction(self, direction: Point) -> None:
        # TODO: round off to closest 8 directions
        self._direction = direction

    def stop(self) -> None:
        """Stop the agent."""
        self._direction = Point(0, 0)

    def get_radius(self) -> int:
        return self.AGENT_RADIUS

    def get_range(self) -> float:
        return self._range

    def set_range(self, range: float) -> None:
        self._range = range

    def get_view_angle(self) -> float:
        return self._view_angle

    def get_view_direction(self) -> Point:
        return self._view_direction

    def set_view_direction(self, view_direction: Point) -> None:
        self._view_direction = view_direction

    def id(self) -> int:
        return self._id

    def get_team(self) -> str:
        return self._team

    def get_fire_time(self) -> int:
        return self._fire_time

    def get_health(self) -> int:
        return self._health

    def fire(self) -> bool:
        if self._fire_time == 0:
            self._fire_time = FIRE_COOLDOWN
            return True
        return False

    def can_fire(self) -> bool:
        return self._fire_time == 0

    def tick(self) -> None:
        """Update the state of the agent by one time step."""
        self._location.add(self._direction)

        if self._fire_time > 0:
            self._fire_time -= 1

    def decrease_health(self, DAMAGE_CAUSED: str) -> None:
        """Decrease the health of the agent."""
        if self._health > 0:
            self._health -= DAMAGES[DAMAGE_CAUSED]
        if self._health < 0:
            self._health = 0

    def set_location(self, location: Point) -> None:
        self._location = location

    def is_alive(self) -> bool:
        return self._health > 0
