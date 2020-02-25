class Agent:

    def __init__(self, agent_attributes):
        for attribute_name, attribute_value in agent_attributes.items():
            setattr(self, attribute_name, attribute_value)


agent_attributes = {
    "age": 50,
    "agreeableness": -0.0909727332893163,
    "conscientiousness": -0.23545266494654954,
    "country_name": "China",
    "country_tld": "cn",
    "date_of_birth": "1967-03-06",
    "extraversion": -0.2889963512006308,
    "id": 265404548,
    "id_str": "yh3-6UC",
    "income": 7751,
    "internet": "false",
    "language": "Xiang",
    "latitude": 29.447948266668902,
    "longitude": 106.56441719305467,
    "neuroticism": -0.023880353116383892,
    "openness": -1.3970222844111286,
    "religion": "folk religion",
    "sex": "Female"
}
agent = Agent(agent_attributes)
print(agent.internet)
