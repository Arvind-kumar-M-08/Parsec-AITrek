from .Point import Point
from constants import UPDATE_DIRECTION, UPDATE_VIEW_DIRECTION, FIRE
# from utils import unformat


class Action:
    _id: int
    agent_id: int
    type: str  # UPDATE_DIRECTION, UPDATE_VIEW_DIRECTION, FIRE
    direction: Point
    STRING: str = "Action with id {id} of type {type} for agent {agent_id} with direction {direction}"

    def __init__(self, agent_id: int, action_type: str, direction: Point):
        # validate the action
        self._id = id(self)
        self.agent_id = agent_id
        self.direction = direction
        if action_type in [UPDATE_DIRECTION, UPDATE_VIEW_DIRECTION, FIRE]:
            self.type = action_type
        else:
            raise ValueError("Invalid action type")

    # def __init__(self, string: str):
    #     parameters = unformat(string, Action.STRING)
    #
    #     if len(parameters) != 4:
    #         raise ValueError("Invalid action string")
    #
    #     # check datatypes
    #     if not isinstance(parameters['id'], int):
    #         raise ValueError("Invalid action id")
    #     if not isinstance(parameters['agent_id'], int):
    #         raise ValueError("Invalid agent id")
    #
    #     if parameters['type'] not in [UPDATE_DIRECTION, UPDATE_VIEW_DIRECTION, FIRE]:
    #         raise ValueError("Invalid action type")
    #
    #     self._id = int(parameters['id'])
    #     self.agent_id = int(parameters['agent_id'])
    #     self.action_type = parameters['type']
    #     self.direction = Point(parameters['direction'])

    def __str__(self):
        return Action.STRING.format(id=self._id, agent_id=self.agent_id, type=self.type, direction=self.direction)

    def __repr__(self):
        return Action.STRING.format(id=self._id, agent_id=self.agent_id, type=self.type, direction=self.direction)
