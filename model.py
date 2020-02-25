import json
import math


class Agent:

    def __init__(self, position, **agent_attributes):
        self.position = position
        for attribute_name, attribute_value in agent_attributes.items():
            setattr(self, attribute_name, attribute_value)


class Position:
    def __init__(self, latitude_degrees, longitude_degrees):
        self.latitude_degrees = latitude_degrees
        self.longitude_degrees = longitude_degrees

    @property
    def longitude(self):
        return self.longitude_degrees * math.pi / 180

    @property
    def latitude(self):
        return self.latitude_degrees * math.pi / 180


def main():
    for agent_attributes in json.load(open("agents-100k.json")):
        latitude = agent_attributes.pop("latitude")
        longitude = agent_attributes.pop("longitude")
        position = Position(latitude, longitude)
        agent = Agent(position, **agent_attributes)
        print(agent.position.longitude)


main()
