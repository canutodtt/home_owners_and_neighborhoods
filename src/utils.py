from src.models import Neighborhood, HomeBuyerAssigner, HomeBuyer


class Parser:
    original_input: str

    def __init__(self, original_input: str) -> None:
        self.original_input = original_input

    @staticmethod
    def parse_to_vectors(vectors_text: list[str]) -> tuple[int, ...]:
        try:
            return tuple(int(vector.split(":")[1]) for vector in vectors_text)
        except ValueError:
            raise ValueError(f"Missing Vectors Values: {vectors_text}")
        except IndexError:
            raise ValueError(f"We require 3 vectors E,W,R given input: {vectors_text}")

    def parse_to_neighborhood(self, neighborhood_text: str) -> Neighborhood:
        data = neighborhood_text.split(" ")
        if len(data) != 5:
            raise ValueError(f"Invalid neighborhood format (N name E W R), given: {neighborhood_text}")
        name = data[1]
        vectors = self.parse_to_vectors(data[2:])
        return Neighborhood(
            name,
            *vectors
        )

    def parse_to_home_buyer(self, home_buyer_text: str) -> HomeBuyer:
        data = home_buyer_text.split(" ")
        if len(data) != 6:
            raise ValueError(f"Invalid home buyer format (H name E W R N_PREFERENCES), given: {home_buyer_text}")
        name = data[1]
        vectors = self.parse_to_vectors(data[2:5])
        preferences = tuple(data[5].split(">"))
        return HomeBuyer(
            name,
            *vectors,
            preferences=preferences
        )

    def parse_to_assigner(self) -> HomeBuyerAssigner:
        assigner = HomeBuyerAssigner()
        lines = self.original_input.splitlines()
        for line in lines:
            if line.startswith("N"):
                assigner.add_neighborhood(self.parse_to_neighborhood(line))
            elif line.startswith("H"):
                assigner.add_home_buyer(self.parse_to_home_buyer(line))
        return assigner


def read_txt_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()
