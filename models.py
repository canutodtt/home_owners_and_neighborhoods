from collections import defaultdict, OrderedDict
from typing import Collection


class BaseModel:
    name: str
    efficiency: int
    water: int
    resilience: int

    def __init__(self, name: str, efficiency: int, water: int, resilience: int):
        self.name = name
        self.efficiency = efficiency
        self.water = water
        self.resilience = resilience

    def __mul__(self, other: 'BaseModel') -> int:
        return sum(x * y for x, y in zip(self.get_metrics, other.get_metrics))

    def __str__(self):
        return self.name

    @property
    def get_metrics(self) -> tuple[int, ...]:
        return self.efficiency, self.water, self.resilience

    # @property
    # def value(self):
    #     return self.efficiency + self.water + self.resilience


class Neighborhood(BaseModel):
    scores: list[tuple[str, int]]

    def __init__(self, name: str, efficiency: int, water: int, resilience: int):
        super().__init__(name, efficiency, water, resilience)
        self.scores = []

    def add_score(self, score: tuple[str, int]) -> None:
        self.scores.append(score)


class HomeBuyer(BaseModel):
    preferences: tuple[str, ...]
    scores: dict[str, int]

    def __init__(self, name: str, efficiency: int, water: int, resilience: int, preferences: tuple[str, ...]):
        super().__init__(name, efficiency, water, resilience)
        self.preferences = preferences
        self.scores = {}

    def calculate_qualifications(self, neighborhood: Neighborhood) -> int:
        score = self * neighborhood
        self.scores[neighborhood.name] = score
        return score

    @property
    def value(self) -> int:
        return sum(self.scores.get(preference, 0) for preference in self.preferences)


class HomeBuyerAssigner:
    neighborhoods: dict[str, Neighborhood]
    home_buyers: dict[str, HomeBuyer]
    assignments: dict[Neighborhood, list[HomeBuyer]]

    def __init__(self):
        self.neighborhoods = {}
        self.home_buyers = {}
        self.assignments = defaultdict(list)

    @property
    def buyers_per_neighborhood(self) -> int:
        total = len(self.home_buyers) / len(self.neighborhoods)
        if total % 1 != 0:
            raise ValueError(
                f'Total number of home buyers per neighborhood must be divisible by {len(self.neighborhoods)}, given {len(self.home_buyers)}''.'
            )
        return int(total)

    def add_neighborhood(self, neighborhood: Neighborhood) -> None:
        self.neighborhoods[neighborhood.name] = neighborhood

    def add_home_buyer(self, home_buyer: HomeBuyer) -> None:
        self.home_buyers[home_buyer.name] = home_buyer
        for neighborhood_name in home_buyer.preferences:
            neighborhood = self.neighborhoods.get(neighborhood_name)
            if neighborhood is None:
                raise ValueError(f'No neighborhood called {neighborhood_name}')
            score = home_buyer.calculate_qualifications(neighborhood)
            neighborhood.add_score((home_buyer.name, score))

    def sorted_neighborhoods_scores(self) -> dict[str, OrderedDict[str, int]]:
        return {name: OrderedDict(sorted(neighborhood.scores, key=lambda x: x[1], reverse=True)) for name, neighborhood
                in self.neighborhoods.items()}

    def sorted_home_buyers(self) -> list[str]:
        return [home_buyer.name for home_buyer in sorted(self.home_buyers.values(), key=lambda x: x.value)]

    def get_first_buyers_scores_for_neighborhood(
        self,
        neighborhood: Neighborhood,
        sorted_scores: OrderedDict[str, int],
        home_buyers: Collection[str]
    ) -> OrderedDict[str, int]:
        scores = []
        counter = 0
        limit = self.buyers_per_neighborhood - len(self.assignments.get(neighborhood, []))
        for i, home_buyer in enumerate(sorted_scores):
            if home_buyer in home_buyers:
                scores.append((home_buyer, sorted_scores.get(home_buyer, 0)))
                counter += 1
            if counter >= limit:
                break
        return OrderedDict(scores)

    def assign_home_buyers(self) -> None:
        self.assignments.clear()
        counter = 0
        home_buyers_to_be_assigned = self.sorted_home_buyers()
        sorted_neighborhoods_scores = self.sorted_neighborhoods_scores()
        while len(home_buyers_to_be_assigned) > 0:
            buyers_assigned = 0
            for home_buyer_name in reversed(home_buyers_to_be_assigned):
                home_buyer = self.home_buyers[home_buyer_name]
                buyer_preference = home_buyer.preferences[counter]
                neighborhood = self.neighborhoods.get(buyer_preference)
                first_elements = OrderedDict(
                    self.get_first_buyers_scores_for_neighborhood(
                        neighborhood,
                        sorted_neighborhoods_scores.get(buyer_preference, {}),
                        home_buyers_to_be_assigned
                    )
                )
                if first_elements.get(home_buyer_name) and len(self.assignments[neighborhood]) < self.buyers_per_neighborhood:
                    self.assignments[neighborhood].append(home_buyer)
                    home_buyers_to_be_assigned.remove(home_buyer_name)
                    buyers_assigned += 1
            if buyers_assigned == 0:
                counter += 1

    def sorted_assignments(self) -> dict[Neighborhood, list[HomeBuyer]]:
        return {
            neighborhood: sorted(buyers, key=lambda x: x.scores.get(neighborhood.name, 0), reverse=True)
            for neighborhood, buyers in self.assignments.items()
        }

    def print_results(self) -> str:
        lines = []
        for neighborhood, home_buyers in sorted(self.sorted_assignments().items(), key=lambda x: str(x[0])):
            line = f"{neighborhood}: "
            for home_buyer in home_buyers:
                line += f"{home_buyer}({home_buyer.scores.get(neighborhood.name, 0)}) "
            lines.append(line)
        return '\n'.join(lines)


def get_first_elements(scores: OrderedDict[str, int], number: int, include: Collection[str]) -> list[tuple[str, int]]:
    elements = []
    counter = 0
    for i, key in enumerate(scores):
        if key in include:
            elements.append((key, scores[key]))
            counter += 1
        if counter == number:
            break
    return elements


def parse_vectors(vectors_text: list[str]) -> tuple[int, ...]:
    try:
        return tuple(int(vector.split(":")[1]) for vector in vectors_text)
    except ValueError:
        raise ValueError(f"Missing Vectors Values: {vectors_text}")
    except IndexError:
        raise ValueError(f"We require 3 vectors E,W,R given input: {vectors_text}")


def parse_neighborhood(neighborhood_text: str) -> Neighborhood:
    data = neighborhood_text.split(" ")
    if len(data) != 5:
        raise ValueError(f"Invalid neighborhood format (N name E W R), given: {neighborhood_text}")
    name = data[1]
    vectors = parse_vectors(data[2:])
    return Neighborhood(
        name,
        *vectors
    )


def parse_home_buyer(home_buyer_text: str) -> HomeBuyer:
    data = home_buyer_text.split(" ")
    if len(data) != 6:
        raise ValueError(f"Invalid home buyer format (H name E W R N_PREFERENCES), given: {home_buyer_text}")
    name = data[1]
    vectors = parse_vectors(data[2:5])
    preferences = tuple(data[5].split(">"))
    return HomeBuyer(
        name,
        *vectors,
        preferences=preferences
    )


def input_parser(input: str) -> HomeBuyerAssigner:
    assigner = HomeBuyerAssigner()
    lines = input.splitlines()
    for line in lines:
        if line.startswith("N"):
            assigner.add_neighborhood(parse_neighborhood(line))
        elif line.startswith("H"):
            assigner.add_home_buyer(parse_home_buyer(line))
    return assigner