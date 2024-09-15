from collections import defaultdict, OrderedDict
from typing import Collection


class BaseModel:
    """
    Base class abstracting general functionality for neighborhoods and home buyers
    """
    name: str
    efficiency: int
    water: int
    resilience: int

    def __init__(self, name: str, efficiency: int, water: int, resilience: int) -> None:
        self.name = name
        self.efficiency = efficiency
        self.water = water
        self.resilience = resilience

    def __mul__(self, other: 'BaseModel') -> int:
        return sum(x * y for x, y in zip(self.vectors, other.vectors))

    def __str__(self) -> str:
        return self.name

    @property
    def vectors(self) -> tuple[int, ...]:
        """
        Returns a tuple with EWR vectors in that order
        """
        return self.efficiency, self.water, self.resilience


class Neighborhood(BaseModel):
    """
    Class representing a neighborhood of home buyers
    """
    scores: list[tuple[str, int]]

    def __init__(self, name: str, efficiency: int, water: int, resilience: int) -> None:
        super().__init__(name, efficiency, water, resilience)
        self.scores = []

    def add_score(self, score: tuple[str, int]) -> None:
        """
        Store home buyer score to the specific neighborhood
        :param score: tuple with home buyer name and score for the neighborhood
        """
        self.scores.append(score)


class HomeBuyer(BaseModel):
    """
    Class representing a home buyer
    """
    preferences: tuple[str, ...]
    scores: dict[str, int]

    def __init__(self, name: str, efficiency: int, water: int, resilience: int, preferences: tuple[str, ...]) -> None:
        super().__init__(name, efficiency, water, resilience)
        self.preferences = preferences
        self.scores = {}

    def calculate_neighborhood_score(self, neighborhood: Neighborhood) -> int:
        """
        Calculate home buyer score for a neighborhood
        :param neighborhood: neighborhood to match with the home buyer
        :return int: home buyer score for the neighborhood
        """
        if not isinstance(neighborhood, Neighborhood):
            raise TypeError(f"input must be an instance of Neighborhood, given {type(neighborhood)}")
        score = self * neighborhood
        self.scores[neighborhood.name] = score
        return score

    @property
    def value(self) -> int:
        """
        Returns the home buyer score for the preferred neighborhood in its list
        :return int: home buyer score for the first neighborhood in its list
        """
        return sum(self.scores.get(preference, 0) for preference in self.preferences)


class HomeBuyerAssigner:
    """
    Class that assigns and classify home buyers to neighborhoods
    """
    neighborhoods: dict[str, Neighborhood]
    home_buyers: dict[str, HomeBuyer]
    assignments: dict[Neighborhood, list[HomeBuyer]]

    def __init__(self) -> None:
        self.neighborhoods = {}
        self.home_buyers = {}
        self.assignments = defaultdict(list)

    @property
    def buyers_per_neighborhood(self) -> int:
        """
        Returns the number of home buyers that each neighborhood must have
        :return int: number of home buyers per neighborhood
        :raises ArithmeticError: if the total number of home buyers per neighborhood is not integer
        :raises ValueError: if there isn't any neighborhood added
        """
        if not self.neighborhoods:
            raise ValueError("No neighborhoods added")
        total = len(self.home_buyers) / len(self.neighborhoods)
        if total % 1 != 0:
            raise ArithmeticError(
                f'Total number of home buyers per neighborhood must be divisible by {len(self.neighborhoods)}, given {len(self.home_buyers)}''.'
            )
        return int(total)

    def add_neighborhood(self, neighborhood: Neighborhood) -> None:
        """
        Add a new neighborhood to the assigner
        :param neighborhood: new neighborhood to be added
        :raises TypeError: if the input does not belong to a Neighborhood instance
        """
        if not isinstance(neighborhood, Neighborhood):
            raise TypeError(f"Input must be an instance of Neighborhood, given {type(neighborhood)}")
        self.neighborhoods[neighborhood.name] = neighborhood

    def add_home_buyer(self, home_buyer: HomeBuyer) -> None:
        """
        Add a new home buyer to the assigner and calculate its scores for its preferred neighborhoods
        :param home_buyer: new home_buyer to be added
        :raises TypeError: if the input does not belong to a HomeBuyer instance
        :raises ValueError: if the home buyer has a non-existent preferred neighborhood
        """
        if not isinstance(home_buyer, HomeBuyer):
            raise TypeError(f"Input must be an instance of Neighborhood, given {type(home_buyer)}")
        self.home_buyers[home_buyer.name] = home_buyer
        # Calculate score for its preferred neighborhoods
        for neighborhood_name in home_buyer.preferences:
            neighborhood = self.neighborhoods.get(neighborhood_name)
            if neighborhood is None:
                raise ValueError(f'No neighborhood called {neighborhood_name}')
            score = home_buyer.calculate_neighborhood_score(neighborhood)
            neighborhood.add_score((home_buyer.name, score))

    def sorted_neighborhoods_scores(self) -> dict[str, OrderedDict[str, int]]:
        """
        Maps each neighborhood with home buyer's scores
        :return: Returns a dictionary that maps each neighborhood with home buyer's scores sorted in descending order
        """
        return {name: OrderedDict(sorted(neighborhood.scores, key=lambda x: x[1], reverse=True)) for name, neighborhood
                in self.neighborhoods.items()}

    def sorted_home_buyers(self) -> list[str]:
        """
        Sort home buyers by their score against their preferred neighborhood
        :return: Returns a sorted home buyers list of names sorted in ascending order
        """
        return [home_buyer.name for home_buyer in sorted(self.home_buyers.values(), key=lambda x: x.value)]

    def get_first_buyers_scores_for_neighborhood(
        self,
        neighborhood: Neighborhood,
        sorted_scores: OrderedDict[str, int],
        home_buyers: Collection[str]
    ) -> OrderedDict[str, int]:
        """
        Gets the remaining home buyers to a neighborhood based on the highest scores
        :param neighborhood: neighborhood to match with the home buyers
        :param sorted_scores: sorted dict of home buyer names to their scores
        :param home_buyers: remaining home buyers to be assigned
        :return: ordered dictionary of best remaining home buyers based on their scores
        """
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
        """
        Assign home buyers to each neighborhood applying the rules of scores and preferred neighborhoods
        """
        self.assignments.clear()
        home_buyers_to_be_assigned = self.sorted_home_buyers()
        sorted_neighborhoods_scores = self.sorted_neighborhoods_scores()
        self.recursive_home_buyers_neighborhoods_match(home_buyers_to_be_assigned, sorted_neighborhoods_scores)

    def recursive_home_buyers_neighborhoods_match(
        self,
        home_buyers_to_be_assigned: list[str],
        sorted_neighborhoods_scores: dict[str, OrderedDict[str, int]],
        neighborhood_index: int = 0
    ) -> None:
        """
        Match home buyers based on their scores against their preferred neighborhoods
        :param home_buyers_to_be_assigned: left home buyers to be assigned
        :param sorted_neighborhoods_scores: mapped neighborhoods with their best home buyers scores
        :param neighborhood_index: preferred neighborhood index
        """
        buyers_assigned = 0
        for home_buyer_name in reversed(home_buyers_to_be_assigned):
            home_buyer = self.home_buyers[home_buyer_name]
            buyer_preference = home_buyer.preferences[neighborhood_index]
            neighborhood = self.neighborhoods.get(buyer_preference)
            first_elements = OrderedDict(
                self.get_first_buyers_scores_for_neighborhood(
                    neighborhood,
                    sorted_neighborhoods_scores.get(buyer_preference, {}),
                    home_buyers_to_be_assigned
                )
            )
            if (
                first_elements.get(home_buyer_name) and
                len(self.assignments[neighborhood]) < self.buyers_per_neighborhood
            ):
                self.assignments[neighborhood].append(home_buyer)
                home_buyers_to_be_assigned.remove(home_buyer_name)
                buyers_assigned += 1
        if buyers_assigned == 0:
            neighborhood_index += 1
        if not home_buyers_to_be_assigned:
            return
        self.recursive_home_buyers_neighborhoods_match(home_buyers_to_be_assigned, sorted_neighborhoods_scores, neighborhood_index)

    def sorted_assignments(self) -> dict[Neighborhood, list[HomeBuyer]]:
        """
        Sort assigned neighborhoods with their home buyers based on the neighborhood name and home buyers score
        :return: mapped dictionary with sorted neighborhoods with their sorted home buyers
        """
        return {
            neighborhood: sorted(buyers, key=lambda x: x.scores.get(neighborhood.name, 0), reverse=True)
            for neighborhood, buyers in self.assignments.items()
        }

    def format_results(self) -> str:
        """
        Format assigned neighborhoods with their home buyers in a valid text string
        :return str: Formatted string of "[Neighborhood name]: [sequence[[Home Buyer name]([Home Buyer Score])]]"
        """
        lines = []
        for neighborhood, home_buyers in sorted(self.sorted_assignments().items(), key=lambda x: str(x[0])):
            line = f"{neighborhood}: "
            for home_buyer in home_buyers:
                line += f"{home_buyer}({home_buyer.scores.get(neighborhood.name, 0)}) "
            lines.append(line)
        return '\n'.join(lines)