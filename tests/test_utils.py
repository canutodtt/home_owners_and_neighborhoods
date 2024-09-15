import unittest

from src.models import Neighborhood, HomeBuyer
from src.utils import Parser


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser("")

    def test_parse_to_vectors(self):
        good_input = ["E:1", "W:2", "R:3"]
        vectors = self.parser.parse_to_vectors(good_input)
        self.assertEqual(vectors, (1, 2, 3))

        missing_input = ["E:1", "R:3"]
        with self.assertRaises(ValueError) as ctx:
            self.parser.parse_to_vectors(missing_input)
        self.assertIn('We require 3 vectors', str(ctx.exception))

        extra_input = ["E:1", "W:2", "R:3", "A:3"]
        with self.assertRaises(ValueError) as ctx:
            self.parser.parse_to_vectors(extra_input)
        self.assertIn('We require 3 vectors', str(ctx.exception))

        bad_input = ["E", "W:2", "R:3"]
        with self.assertRaises(ValueError) as ctx:
            self.parser.parse_to_vectors(bad_input)
        self.assertIn('We require the format', str(ctx.exception))

        wrong_input = ["E:a", "W:2", "R:3"]
        with self.assertRaises(ValueError) as ctx:
            self.parser.parse_to_vectors(wrong_input)
        self.assertIn('Some Values aren\'t integers', str(ctx.exception))

    def test_parse_to_neighborhood(self):
        neighborhood = self.parser.parse_to_neighborhood("N N0 E:7 W:7 R:10")
        expected_neighborhood = Neighborhood('N0', 7, 7, 10)
        self.assertEqual(neighborhood.name, expected_neighborhood.name)
        self.assertEqual(neighborhood.vectors, expected_neighborhood.vectors)
        self.assertEqual(neighborhood.scores, expected_neighborhood.scores)

        with self.assertRaises(ValueError):
            self.parser.parse_to_neighborhood("N N0 E:7 W:7")

        with self.assertRaises(ValueError):
            self.parser.parse_to_neighborhood("N N0 E:7 W:7 R:10 H:2")

    def test_parse_to_home_buyer(self):
        home_buyer = self.parser.parse_to_home_buyer("H H0 E:7 W:7 R:10 N0")
        expected_home_buyer = HomeBuyer('H0', 7, 7, 10, ('N0',))
        self.assertEqual(home_buyer.name, expected_home_buyer.name)
        self.assertEqual(home_buyer.vectors, expected_home_buyer.vectors)
        self.assertEqual(home_buyer.preferences, expected_home_buyer.preferences)
        self.assertEqual(home_buyer.scores, expected_home_buyer.scores)

        with self.assertRaises(ValueError):
            self.parser.parse_to_home_buyer("H H0 E:7 W:7 R:10")

        with self.assertRaises(ValueError):
            self.parser.parse_to_home_buyer("H H0 E:7 W:7 R:10 H:2 N0>N1")

    def test_parse_to_assigner(self):
        text = "N N0 E:1 W:1 R:1\nN N1 E:2 W:2 R:2\nH H0 E:3 W:3 R:3 N0>N1\nH H1 E:4 W:4 R:4 N1>N0"
        self.parser = Parser(text)
        assigner = self.parser.parse_to_assigner()
        self.assertEqual(len(assigner.neighborhoods), 2)
        self.assertEqual(len(assigner.home_buyers), 2)