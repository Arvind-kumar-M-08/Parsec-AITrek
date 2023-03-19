AI Trek Documentation
=========================

## <b> Agent.py </b>

Represents an agent.

### Attributes
----------------

*   `AGENT_RADIUS: int` - Radius of the agent
*   `_location: Point` - Current location of the agent
*   `_direction: Point` - Angle in which the agent is going
*   `_range: float` - Range of the agent's view
*   `_view_angle: float` - Agent's view angle in radians. $\pi/2$ means the agent can view $+90 \degree$ to $-90 \degree$ (total $180 \degree$)
*   `_view_direction: Point` - Angle in which the agent is facing
*   `_fire_time: int` - Time until the agent can fire again
*   `_health: int` - Health of the agent
*   `_team: str` - Team which the agent belongs to
*   `_id: int` - Auto generated ID of the agent

### Methods
--------

*   `__str__(self) -> str` - Return a string representation of the agent.
*   `get_location(self) -> Point` - Get the current location of the agent.
*   `get_direction(self) -> Point` - Get the current direction of the agent.
*   `set_direction(self, direction: Point) -> None` - Set the direction of the agent.
*   `stop(self) -> None` - Stop the agent.
*   `get_radius(self) -> int` - Get the radius of the agent.
*   `get_range(self) -> float` - Get the range of the agent's view.
*   `set_range(self, range: float) -> None` - Set the range of the agent's view.
*   `get_view_angle(self) -> float` - Get the view angle of the agent.
*   `get_view_direction(self) -> Point` - Get the view direction of the agent.
*   `set_view_direction(self, view_direction: Point) -> None` - Set the view direction of the agent.
*   `id(self) -> int` - Get the ID of the agent.
*   `get_team(self) -> str` - Get the team of the agent.
*   `get_fire_time(self) -> int` - Get the time until the agent can fire again.
*    `get_health(self) -> int` - Get the health of the agent.
*    `fire(self) -> bool` - Fire the agent's weapon if the weapon is not on cooldown.
*   `can_fire(self) -> bool` - Check if the agent's weapon is off cooldown and can be fired.
*   `tick(self) -> None` - Update the state of the agent by one time step.
*    `decrease_health(self, DAMAGE_CAUSED: str) -> None` - Decrease the health of the agent.
*   `set_location(self, location: Point) -> None` - Set the location of the agent to the specified point.
*   `is_alive(self) -> bool` - Check if the agent is still alive based on its health.

------
------

## <b> Action.py </b>

Models actions which can be taken by agents.

### Attributes
--------

* `_id: int` - A unique identifier for the action instance.
* `agent_id: int` - The identifier of the agent that performs the action.
* `type: str` - The type of the action, which can be one of the following: `UPDATE_DIRECTION`, `UPDATE_VIEW_DIRECTION`, `FIRE`.
* `direction: Point` - A `Point` object representing the direction of the action.

### Methods
--------

* `__str__(self)` - Returns a string representation of the action.
* `__repr__(self)` - Returns a string representation of the action that can be used to recreate the instance.

------
------

## <b> Alert.py </b>

Models alerts.

### Attributes
--------

* `_id: int` - A unique identifier for the alert instance.
* `alert_type: str` - The type of the alert, which can be one of the following: `COLLISION`, `ZONE`, `BULLET_HIT`, or `DEAD`.
* `agent_id: int` - The identifier of the agent that receives the alert.

### Methods
--------

* `__init__(self, alert_type: str, agent_id: int)` - Initializes an alert instance with the given alert type and agent ID.
* `__str__(self)` - Returns a string representation of the alert.
* `__repr__(self)` - Returns a string representation of the alert that can be used to recreate the instance.

------
------

## <b> Bullet.py </b>

Models a bullet.

### Attributes
--------

* `_location: Point` - A `Point` object representing the location of the bullet.
* `_direction: Point` - A `Point` object representing the direction of the bullet. Only 8 directions are possible, and 0,0 is allowed for stopping.
* `_energy: int` - An integer representing the energy or "life" of the bullet.
* `_id: int` - A unique identifier for the bullet instance.

### Methods
--------

* `get_direction(self) -> Point` - Returns the direction of the bullet.
* `get_energy(self) -> int` - Returns the energy of the bullet.
* `tick(self) -> None` - Moves the bullet in its current direction and reduces its energy by 1.
* `is_alive(self) -> bool` - Returns `True` if the bullet has energy remaining, `False` otherwise.
* `get_location(self) -> Point` - Returns the location of the bullet.
* `is_colliding_with_agent(self, agent: Agent) -> bool` - Returns `True` if the bullet is colliding with the given agent, `False` otherwise.
* `is_colliding_with_obstacle(self, obstacle: Obstacle) -> bool` - Returns `True` if the bullet is colliding with the given obstacle, `False` otherwise.
* `is_colliding(self, obj: Obstacle or Agent) -> bool` - Returns `True` if the bullet is colliding with the given obstacle or agent, `False` otherwise.
* `dead(self) -> None` - Sets the energy of the bullet to 0.

------
------

## <b> Line.py </b>

Models a line in the game.

### Attributes
--------

- `p1`: instance of `Point` class representing the first endpoint of the line.
- `p2`: instance of `Point` class representing the second endpoint of the line.

### Methods
--------

- `__str__(self)`: Returns a string representation of the `Line` object.
- `__repr__(self)`: Returns a string representation of the `Line` object.
- `onLine(self, p: Point)`: Determines whether the given point `p` lies on the line.
- `direction(a: Point, b: Point, c: Point)`: Computes the direction of the turn formed by three points `a`, `b`, and `c`.
- `isIntersect(self, l2)`: Determines whether the current line intersects with another line `l2`.

------
------

## <b> ObjectSighting.py </b>

Models objects which can be viewed by agents.

### Attributes:

- `object_type`: str - Opponent's Agent, Bullet
- `location`: Point - location of the object
- `direction`: Point - direction of the object. For Wall it's Point(0,0)
- `_id`: int - unique identifier of the object sighting

### Methods:

- `__str__()`: returns a string representation of the object sighting
- `__repr__()`: returns a string representation of the object sighting

------
------

## <b> Obstacle.py </b>

This class represents a polygonal obstacle in the game.

### Attributes

- `corners`: A list of `Point` objects representing the corners of the obstacle.
- `n`: An integer representing the number of corners.
- `STRING`: A class variable containing the string representation of an `Obstacle` object.

### Methods

- `__str__(self)`: Returns a string representation of the `Obstacle` object.
- `__repr__(self)`: Returns a string representation of the `Obstacle` object.
- `intersects_circle(self, center: Point, radius: float) -> bool`: Returns `True` if the obstacle intersects with the circle defined by the `center` and `radius`.
- `checkInside(self, p: Point) -> bool`: Returns `True` if the given `Point` object `p` is inside the obstacle.
- `get_edges(self) -> List[Line]`: Returns a list of `Line` objects representing the edges of the obstacle.

------
------

## <b> Point.py </b>

A model of a 2-d cartesian coordinate Point.

### Properties

- `x`: `float` - X coordinate
- `y`: `float` - Y coordinate

### Methods

- `__init__(self, x: float, y: float)`: Construct a point with x, y coordinates.
- `add(self, other)`: Add two Point objects together and return a new Point.
- `sub(self, other)`: Subtract two Point objects and return a new Point.
- `distance(self, other) -> float`: Return the distance between two points.
- `make_unit_magnitude(self)`: Return the unit vector of the point.
- `get_angle(self) -> float`: Return the angle of the point.
- `__str__(self) -> str`: Return a string representation of the point.
- `__repr__(self) -> str`: Return a string representation of the point.

------
------

## <b> State.py </b>

The `State` class represents the current state of the game environment. It contains information about the player's agents, objects in sight, alerts, team, time, obstacles, zone, safe zone, and whether the zone is shrinking.

### Properties

- `agents`: A dictionary of `Agent` objects representing the player's agents.
- `object_in_sight`: A dictionary of lists of `ObjectSighting` objects representing objects in sight of agents and bullets.
- `alerts`: A list of `Alert` objects representing various alerts such as collisions, zone, bullet_hit, etc.
- `team`: A string representing the player's team.
- `time`: An integer representing the current time.
- `obstacles`: A list of `Obstacle` objects representing obstacles in the environment.
- `zone`: A list of `Point` objects representing the corners of the zone.
- `safe_zone`: A list of `Point` objects representing the corners of the safe zone.
- `is_zone_shrinking`: A boolean representing whether the zone is shrinking or not.

### Methods

- `__str__()`: Returns a formatted string representation of the `State` object.
- `__repr__()`: Returns a string representation of the `State` object.

------
------





