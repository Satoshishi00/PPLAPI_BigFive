# -*-coding:Latin-1 -*

import math
import json
import matplotlib.pyplot as plt


class Agent:

    def __init__(self, position, **agent_attributes):
        self.position = position
        for attribute_name, attribute_value in agent_attributes.items():
            setattr(self, attribute_name, attribute_value)


class Position:
    def __init__(self, longitude_degrees, latitude_degrees):
        self.longitude_degrees = longitude_degrees
        self.latitude_degrees = latitude_degrees

    @property
    def longitude(self):
        return self.longitude_degrees * math.pi / 180

    @property
    def latitude(self):
        return self.latitude_degrees * math.pi / 180


class Zone:

    ZONES = []
    EARTH_RADIUS_KILOMETERS = 6371
    MIN_LONGITUDE_DEGREES = -180
    MAX_LONGITUDE_DEGREES = 180
    MIN_LATITUDE_DEGREES = -90
    MAX_LATITUDE_DEGREES = 90
    WIDTH_DEGREES = 1
    HEIGHT_DEGREES = 1

    def __init__(self, corner1, corner2):
        self.corner1 = corner1
        self.corner2 = corner2
        self.inhabitants = []

    @classmethod
    def _initialize_zones(cls):
        for latitude in range(cls.MIN_LATITUDE_DEGREES, cls.MAX_LATITUDE_DEGREES, cls.HEIGHT_DEGREES):
            for longitude in range(cls.MIN_LONGITUDE_DEGREES, cls.MAX_LONGITUDE_DEGREES, cls.WIDTH_DEGREES):
                bottom_left_corner = Position(longitude, latitude)
                top_right_corner = Position(
                    longitude + cls.WIDTH_DEGREES, latitude + cls.HEIGHT_DEGREES)
                zone = Zone(bottom_left_corner, top_right_corner)
                cls.ZONES.append(zone)
        print(len(cls.ZONES))

    # Verifie qu'une position appartient bien à une zone
    def contains(self, position):
        return position.longitude >= min(self.corner1.longitude, self.corner2.longitude) and \
            position.longitude < max(self.corner1.longitude, self.corner2.longitude) and \
            position.latitude >= min(self.corner1.latitude, self.corner2.latitude) and \
            position.latitude < max(
                self.corner1.latitude, self.corner2.latitude)

    @classmethod
    # Retourne la zone à laquelle appartient une position
    def find_zone_that_contains(cls, position):
        if not cls.ZONES:
            # Initialisation de la grille et de ses zones
            cls._initialize_zones()
        # Détermination de l'index de la zone à laquelle appartient une position
        longitude_index = int(
            (position.longitude_degrees - cls.MIN_LONGITUDE_DEGREES) / cls.WIDTH_DEGREES)
        latitude_index = int(
            (position.latitude_degrees - cls.MIN_LATITUDE_DEGREES) / cls.HEIGHT_DEGREES)
        longitude_bins = int(
            (cls.MAX_LONGITUDE_DEGREES - cls.MIN_LONGITUDE_DEGREES) / cls.WIDTH_DEGREES)
        zone_index = latitude_index * longitude_bins + longitude_index

        zone = cls.ZONES[zone_index]
        # Vérification de que la position puisse bien appartenir à cette zone
        assert zone.contains(position)

        return zone

    def add_inhabitant(self, inhabitant):
        self.inhabitants.append(inhabitant)

    @property
    def population(self):
        return len(self.inhabitants)

    @property
    def width(self):
        return abs(self.corner1.longitude - self.corner2.longitude) * self.EARTH_RADIUS_KILOMETERS

    @property
    def height(self):
        return abs(self.corner1.latitude - self.corner2.latitude) * self.EARTH_RADIUS_KILOMETERS

    @property
    def area(self):
        return self.height * self.width

    def population_density(self):
        return self.population / self.area

    def average_agreeableness(self):
        if not self.inhabitants:
            return 0
        return sum([inhabitant.agreeableness for inhabitant in self.inhabitants]) / self.population


class BaseGraph:

    def __init__(self):
        self.title = "Title graph"
        self.x_label = "X"
        self.y_label = "Y"
        self.show_grid = True

    def show(self, zones):
        x_values, y_values = self.xy_values(zones)
        plt.plot(x_values, y_values, '.')
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.title)
        plt.grid(self.show_grid)
        plt.show()

    def xy_values(self, zones):
        # Forcer la définition de la methode dans l'enfant (methode abstraite)
        raise NotImplementedError

# AgreeablenessGraph hérite de BaseGraph


class AgreeablenessGraph(BaseGraph):

    def __init__(self):
        super().__init__()
        self.title = "People agreebleness"
        self.x_label = "population density"
        self.y_label = "agreeableness"

    def xy_values(self, zones):
        x_values = [zone.population_density() for zone in zones]
        y_values = [zone.average_agreeableness() for zone in zones]
        return x_values, y_values


class IncomesGraph(BaseGraph):

    def __init__(self):
        super().__init__()
        self.title = "Incomes in age"
        self.x_label = "Age"
        self.y_label = "Incomes"

    def xy_values(self, zones):
        x_values = zones[0]
        y_values = zones[1]
        return x_values, y_values


def main():
    # Initialisation des tableaux pour déterminer les revenus en fonction de l'age
    age_numbers = []
    sum_incomes = []
    for i in range(0, 100):
        age_numbers.append(0)
        sum_incomes.append(0)

    for agent_attributes in json.load(open("agents-100k.json")):
        # Détermination de la position de l'agent
        longitude = agent_attributes.pop("longitude")
        latitude = agent_attributes.pop("latitude")
        position = Position(longitude, latitude)
        # Création de l'agent
        agent = Agent(position, **agent_attributes)
        # Enregistrement de l'agent dans la zone correspondant à sa position
        zone = Zone.find_zone_that_contains(position)
        zone.add_inhabitant(agent)

        # Récupération du nombre de personne et des revenus
        age_numbers[agent.age] += 1
        sum_incomes[agent.age] += agent.income

    # Graph initialization
    agreeableness_graph = AgreeablenessGraph()
    # Show graph
    agreeableness_graph.show(Zone.ZONES)

    # Récupération de l'age et des revenus moyens
    age = []
    incomes = []
    for i in range(0, 100):
        age.append(i)
        # Pour éviter la division par 0
        if age_numbers[i] == 0:
            age_numbers[i] = 1
        incomes.append(sum_incomes[i]/age_numbers[i])

    # Affichage du graphique des revenus en fonction de l'age
    incomes_graph = IncomesGraph()
    incomes_graph.show([age, incomes])


main()
