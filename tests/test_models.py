import unittest
from collections import OrderedDict

from src.models import BaseModel, Neighborhood, HomeBuyer, HomeBuyerAssigner


class TestBaseModel(unittest.TestCase):
    def test_happy_path(self):
        vectors = (1, 2, 3)
        name = "B0"
        model = BaseModel(name, *vectors)
        self.assertEqual(model.name, name)
        self.assertEqual(model.vectors, vectors)
        self.assertEqual(str(model), name)
        self.assertEqual(model * model, sum(vector ** 2 for vector in vectors))


class TestNeighborhood(unittest.TestCase):
    def test_add_score(self):
        vectors = (1, 2, 3)
        name = "N0"
        neighborhood = Neighborhood(name, *vectors)
        self.assertEqual(neighborhood.name, name)
        self.assertEqual(neighborhood.vectors, vectors)

        neighborhood.add_score(('H0', 11))
        self.assertEqual(neighborhood.scores[0], ('H0', 11))


class TestHomeBuyer(unittest.TestCase):
    def setUp(self):
        self.vectors = (1, 2, 3)
        self.name = "H0"
        self.neighborhood_name = "N0"
        self.neighborhood = Neighborhood(self.neighborhood_name, *self.vectors)

    def test_calculate_neighborhood_score_happy_path(self):
        home_buyer = HomeBuyer(self.name, *self.vectors, preferences=(self.neighborhood_name,))

        score = home_buyer.calculate_neighborhood_score(self.neighborhood)
        expected_score = sum(vector ** 2 for vector in self.vectors)

        self.assertEqual(score, expected_score)
        self.assertEqual(home_buyer.value, expected_score)

    def test_calculate_neighborhood_score_wrong_path(self):
        home_buyer = HomeBuyer(self.name, *self.vectors, preferences=(self.neighborhood_name,))

        with self.assertRaises(TypeError):
            home_buyer.calculate_neighborhood_score(self.neighborhood_name)  # noqa

        self.assertEqual(home_buyer.value, 0)


class TestHomeBuyerAssigner(unittest.TestCase):
    def setUp(self):
        self.neighborhoods = [
            Neighborhood('N0', 7, 7, 10),
            Neighborhood('N1', 2, 1, 1),
            Neighborhood('N2', 7, 6, 4),
        ]
        self.home_buyers = [
            HomeBuyer('H0', 3, 9, 2, ('N2', 'N0', 'N1')),
            HomeBuyer('H0', 3, 9, 2, ('N2', 'N0', 'N1')),
            HomeBuyer('H1', 4, 3, 7, ('N0', 'N2', 'N1')),
            HomeBuyer('H2', 4, 0, 10, ('N0', 'N2', 'N1')),
            HomeBuyer('H3', 10, 3, 8, ('N2', 'N0', 'N1')),
            HomeBuyer('H4', 6, 10, 1, ('N0', 'N2', 'N1')),
            HomeBuyer('H5', 6, 7, 7, ('N0', 'N2', 'N1')),
            HomeBuyer('H6', 8, 6, 9, ('N2', 'N1', 'N0')),
            HomeBuyer('H7', 7, 1, 5, ('N2', 'N1', 'N0')),
            HomeBuyer('H8', 8, 2, 3, ('N1', 'N0', 'N2')),
            HomeBuyer('H9', 10, 2, 1, ('N1', 'N2', 'N0')),
            HomeBuyer('H10', 6, 4, 5, ('N0', 'N2', 'N1')),
            HomeBuyer('H11', 8, 4, 7, ('N0', 'N1', 'N2')),
        ]

    def setup_assigner(self) -> HomeBuyerAssigner:
        assigner = HomeBuyerAssigner()
        [assigner.add_neighborhood(neighborhood) for neighborhood in self.neighborhoods]
        [assigner.add_home_buyer(home_buyers) for home_buyers in self.home_buyers]
        return assigner

    def test_properties_happy_path(self):
        assigner = HomeBuyerAssigner()
        assigner.add_neighborhood(self.neighborhoods[0])
        self.assertEqual(assigner.buyers_per_neighborhood, 0)
        self.assertEqual(len(assigner.neighborhoods), 1)
        self.assertEqual(len(assigner.home_buyers), 0)
        self.assertEqual(assigner.assignments, {})

    def test_properties_wrong_path(self):
        assigner = HomeBuyerAssigner()
        with self.assertRaises(ValueError):
            # test it fails as len of neighborhoods can raise a division by 0
            _ = assigner.buyers_per_neighborhood

        [assigner.add_neighborhood(neighborhood) for neighborhood in self.neighborhoods]
        assigner.add_home_buyer(self.home_buyers[0])
        with self.assertRaises(ArithmeticError):
            # test it fails as 1 home buyer can't be equally assigned to many neighborhoods
            _ = assigner.buyers_per_neighborhood

    def test_add_neighborhood(self):
        assigner = HomeBuyerAssigner()
        [assigner.add_neighborhood(neighborhood) for neighborhood in self.neighborhoods]

        self.assertEqual(len(assigner.neighborhoods), len(self.neighborhoods))

        with self.assertRaises(TypeError):
            assigner.add_neighborhood("test")  # noqa

    def test_add_home_buyer(self):
        assigner = HomeBuyerAssigner()

        with self.assertRaises(ValueError):
            # fail as none neighborhood where added previously
            assigner.add_home_buyer(self.home_buyers[0])

        with self.assertRaises(TypeError):
            # fail validation input
            assigner.add_home_buyer("test")  # noqa

        [assigner.add_neighborhood(neighborhood) for neighborhood in self.neighborhoods]
        for home_buyer in self.home_buyers:
            # scores are not yet calculated
            self.assertEqual(home_buyer.scores, {})
        [assigner.add_home_buyer(home_buyers) for home_buyers in self.home_buyers]
        for home_buyer in self.home_buyers:
            # scores were calculated for all the neighborhoods
            self.assertEqual(len(home_buyer.scores), len(self.neighborhoods))

    def test_sorted_neighborhoods_scores(self):
        assigner = self.setup_assigner()
        sorted_neighborhoods_scores = assigner.sorted_neighborhoods_scores()
        expected_neighborhoods_scores = {
            'N0': OrderedDict(
                [('H6', 188), ('H3', 171), ('H5', 161), ('H11', 154), ('H2', 128), ('H4', 122), ('H10', 120),
                 ('H1', 119), ('H7', 106), ('H0', 104), ('H8', 100), ('H9', 94)]),
            'N1': OrderedDict(
                [('H3', 31), ('H6', 31), ('H11', 27), ('H5', 26), ('H4', 23), ('H9', 23), ('H8', 21), ('H10', 21),
                 ('H7', 20), ('H1', 18), ('H2', 18), ('H0', 17)]),
            'N2': OrderedDict(
                [('H6', 128), ('H3', 120), ('H5', 112), ('H11', 108), ('H4', 106), ('H9', 86), ('H10', 86), ('H0', 83),
                 ('H8', 80), ('H7', 75), ('H1', 74), ('H2', 68)])
        }
        self.assertEqual(sorted_neighborhoods_scores, expected_neighborhoods_scores)

    def test_sorted_home_buyers(self):
        assigner = self.setup_assigner()
        sorted_home_buyers = assigner.sorted_home_buyers()
        expected_home_buyers_sorted = ['H7', 'H8', 'H9', 'H0', 'H1', 'H2', 'H10', 'H4', 'H11', 'H5', 'H3', 'H6']
        self.assertEqual(sorted_home_buyers, expected_home_buyers_sorted)

    def test_get_first_buyers_scores_for_neighborhood(self):
        assigner = self.setup_assigner()
        neighborhood = self.neighborhoods[0]
        sorted_scores = OrderedDict(
            [('H6', 188), ('H3', 171), ('H5', 161), ('H11', 154), ('H2', 128), ('H4', 122), ('H10', 120), ('H1', 119),
             ('H7', 106), ('H0', 104), ('H8', 100), ('H9', 94)])
        home_buyers = [str(home_buyer) for home_buyer in self.home_buyers]
        scores = assigner.get_first_buyers_scores_for_neighborhood(neighborhood, sorted_scores, home_buyers)
        expected_scores = OrderedDict([('H6', 188), ('H3', 171), ('H5', 161), ('H11', 154)])
        self.assertEqual(scores, expected_scores)

    def test_assign_home_buyers(self):
        assigner = self.setup_assigner()
        assigner.assign_home_buyers()
        expected_assignment = {
            self.neighborhoods[0]: ['H5', 'H11', 'H2', 'H4'],
            self.neighborhoods[1]: ['H9', 'H8', 'H7', 'H1'],
            self.neighborhoods[2]: ['H6', 'H3', 'H10', 'H0'],
        }
        for neighborhood, home_buyers in expected_assignment.items():
            self.assertIn(neighborhood, assigner.assignments)
            for home_buyer in assigner.assignments[neighborhood]:
                self.assertIn(home_buyer.name, home_buyers)

    def test_format_results(self):
        assigner = self.setup_assigner()
        assigner.assign_home_buyers()
        text = assigner.format_results()
        expected_result = (
            "N0: H5(161) H11(154) H2(128) H4(122) \n"
            "N1: H9(23) H8(21) H7(20) H1(18) \n"
            "N2: H6(128) H3(120) H10(86) H0(83) \n"
        )
        self.assertEqual(text.strip(), expected_result.strip())
