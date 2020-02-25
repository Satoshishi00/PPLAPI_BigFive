import json


class Agent:

    def __init__(self, **agent_attributes):
        for attribute_name, attribute_value in agent_attributes.items():
            setattr(self, attribute_name, attribute_value)


def main():
    for agent_attributes in json.load(open("agents-100k.json")):
        agent = Agent(**agent_attributes)
        print(agent.agreeableness)


main()
