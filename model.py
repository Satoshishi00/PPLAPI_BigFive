class Agent:

    def __init__(self, agreeableness):
        self.agreeableness = agreeableness

    def say_hello(self, name):
        return "Bien le bonjour " + name + " !"


agent = Agent(10)
print(agent.agreeableness)
